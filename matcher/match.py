import json
import logging
import flask
import pandas
from . import model
from . import sql_functions
from . import standardisation_functions
from textdistance import levenshtein, jaro_winkler
from flaskr.db import get_db

bp = flask.Blueprint('match', __name__, url_prefix='/match')


@bp.route('/match', methods=['POST'])
def match():
    logging.info("match requested")
    df = pandas.read_json(json.dumps(flask.request.get_json()), dtype=str)

    data = standardisation_functions.standardise_pnc_number(df=df, pnc_col='pnc_number')
    data = standardisation_functions.standardise_dob(data, dob_col='dob')
    data = standardisation_functions.standardise_names(df=data, name_cols=['first_name', 'surname'])
    data = standardisation_functions.fix_zero_length_strings(data)

    response = score(data)
    logging.info("match completed")
    return response


def score(data):
    with get_db() as conn:
        c = conn.cursor()

        # Register SQL functions
        # TODO register functions once on startup
        conn.create_function("concat", -1, sql_functions.concat)
        conn.create_function("jaro_winkler_sim", 2, jaro_winkler)
        conn.create_function("Dmetaphone", 1, sql_functions.Dmetaphone)
        conn.create_function("levenshtein", 2, levenshtein)
        conn.create_function("datediff", 2, sql_functions.datediff)

        # TODO create unique database tables
        data.to_sql(name='df', con=conn, if_exists='replace', index=False)
        c.execute(f"""CREATE TABLE df_comparison AS {model.df_comparison}""")
        c.execute(f"""CREATE TABLE df_with_gamma AS {model.df_with_gamma}""")
        c.execute(f"""CREATE TABLE df_with_gamma_probs AS {model.df_with_gamma_probs}""")
        c.execute(f"""CREATE TABLE df_e AS {model.df_e}""")

        json_output = pandas.read_sql("""select * from df_e""", con=conn).to_json()
        # TODO remove PII from logging
        logging.info({
            'msg': 'scored outcome',
            'read_sql': json_output,
        })

        # TODO clean up database tables reliably
        c.execute(f"""DROP TABLE IF EXISTS df_comparison""")
        c.execute(f"""DROP TABLE IF EXISTS df_with_gamma""")
        c.execute(f"""DROP TABLE IF EXISTS df_with_gamma_probs""")
        c.execute(f"""DROP TABLE IF EXISTS df_e""")

        return json.loads(json_output)


class UnsupportedError(Exception):
    fmt = 'unsupported request'
