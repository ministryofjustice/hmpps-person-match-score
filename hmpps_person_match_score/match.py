import json
import logging
import flask
import pandas as pd
from hmpps_person_match_score.utility_functions.demo_utils import get_spark
from hmpps_person_match_score.standardisation_functions.names import standardise_names
from hmpps_person_match_score.standardisation_functions.date_of_birth import standardise_dob, null_suspicious_dob_std
from hmpps_person_match_score.standardisation_functions.fix_string import fix_zero_length_strings
from hmpps_person_match_score.standardisation_functions.pnc_number import standardise_pnc_number
from splink.model import load_model_from_json
from splink.blocking import block_using_rules
from splink.gammas import add_gammas
from splink.expectation_step import run_expectation_step

blueprint = flask.Blueprint('match', __name__)


@blueprint.route('/ping', methods=['GET'])
def ping():
    return "pong"


@blueprint.route('/match', methods=['POST'])
def match():

    logging.info("Match score requested")
    
    # spark session
    spark = get_spark()
    
    data = pd.read_json(json.dumps(flask.request.get_json()), dtype=str)
    df = spark.createDataFrame(data)

    # standardise
    df_std_names = standardise_names(df=df, name_cols=["first_name", "surname"]) 
    df_std_dob = standardise_dob(df=df_std_names, dob_col="dob") 
    df_std_dob_null = null_suspicious_dob_std(df=df_std_dob, dob_col="dob_std") 
    df_pnc_std = standardise_pnc_number(df=df_std_dob_null, pnc_col="pnc_number")
    df_std = fix_zero_length_strings(df=df_pnc_std)
    
    # import model
    saved_model = load_model_from_json("model/saved_model.json")

    response = score(df_std)
    logging.info("Match score completed")
    return response


def score(data):
    
    df_comparison = block_using_rules(settings=saved_model.current_settings_obj.settings_dict, df=data, spark=spark) 
    df_gammas = add_gammas(df_comparison=df_comparison, settings_dict=saved_model.current_settings_obj.settings_dict, spark=spark) 
    df_e = run_expectation_step(df_with_gamma=df_gammas, model=saved_model, spark=spark)
    
    json_output = df_e.toPandas().to_json()
        # TODO remove PII from logging
    logging.info({
        'msg': 'scored outcome', 
        'read_sql': json_output
    })
    
    return json.loads(json_output)


class UnsupportedError(Exception):
    fmt = 'unsupported request'
