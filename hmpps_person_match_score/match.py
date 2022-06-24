import time
import json
import logging
import flask
import pandas as pd
from .spark import spark
from hmpps_person_match_score.standardisation_functions.names import standardise_names
from hmpps_person_match_score.standardisation_functions.date_of_birth import standardise_dob, null_suspicious_dob_std
from hmpps_person_match_score.standardisation_functions.fix_string import fix_zero_length_strings
from hmpps_person_match_score.standardisation_functions.pnc_number import standardise_pnc_number
from splink.blocking import block_using_rules
from splink.gammas import add_gammas
from splink.expectation_step import run_expectation_step
from hmpps_person_match_score.model.model import get_model

blueprint = flask.Blueprint('match', __name__)


def log_time(msg, start_time=time.time_ns()):
    end_time = time.time_ns()
    logging.info(">>>>>>>>>> " + msg + " " + str(int((end_time - start_time) / 1000000)) + "ms")
    return end_time


@blueprint.route('/ping', methods=['GET'])
def ping():
    return "pong"


@blueprint.route('/match', methods=['POST'])
def match():
    logging.info("Match score requested")
    data = pd.read_json(json.dumps(flask.request.get_json()), dtype=str)
    response = score(data)
    logging.info("Match score completed")
    return response


def score(data):
    t = log_time("Start score")

    # spark session
    spark = get_spark()
    t = log_time("get_spark()", t)

    # import model
    saved_model = get_model()
    t = log_time("get_model()", t)

    # standardise
    df = spark.createDataFrame(data)
    df_std_names = standardise_names(df=df, name_cols=["first_name", "surname"])
    df_std_dob = standardise_dob(df=df_std_names, dob_col="dob")
    df_std_dob_null = null_suspicious_dob_std(df=df_std_dob, dob_col="dob_std")
    df_pnc_std = standardise_pnc_number(df=df_std_dob_null, pnc_col="pnc_number")
    df_std = fix_zero_length_strings(df=df_pnc_std)
    t = log_time("standardise", t)

    # score
    df_comparison = block_using_rules(settings=saved_model.current_settings_obj.settings_dict, df=df_std, spark=spark)
    df_gammas = add_gammas(df_comparison=df_comparison, settings_dict=saved_model.current_settings_obj.settings_dict,
                           spark=spark)
    df_e = run_expectation_step(df_with_gamma=df_gammas, model=saved_model, spark=spark)
    t = log_time("score", t)

    json_output = df_e.toPandas().to_json()
    # TODO remove PII from logging
    logging.info({
        'msg': 'scored outcome',
        'read_sql': json_output
    })

    log_time("End score", t)

    return json.loads(json_output)


def get_spark():
    if 'spark' not in flask.g:
        jars = flask.current_app.config['JARS']
        flask.g.spark = spark(jars)

    return flask.g.spark


class UnsupportedError(Exception):
    fmt = 'unsupported request'
