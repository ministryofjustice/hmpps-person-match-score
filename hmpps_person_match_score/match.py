import json
import flask
import pandas
from textdistance import levenshtein, jaro_winkler
from .db import get_db
from . import model
from . import sql_functions
from . import standardisation_functions
from hmpps_person_match_score.app_insights import logger, event_logger

blueprint = flask.Blueprint('match', __name__)


@blueprint.route('/ping', methods=['GET'])
def ping():
    try:
        return "pong"
    except Exception as e:
        logger(__name__).exception('Exception at ping endpoint')
        return e.args[0], 500

@blueprint.route('/health', methods=['GET'])
def health():
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1')
            result = cursor.fetchone()
            return result is not None and 'UP'
    except Exception as e:
        logger.exception('Exception at health endpoint')
        return 'DOWN', 503


@blueprint.route('/match', methods=['POST'])
def match():
    try:
        data = pandas.read_json(json.dumps(flask.request.get_json()), dtype=str)

        data = standardisation_functions.standardise_pnc_number(data, pnc_col='pnc_number')
        data = standardisation_functions.standardise_dob(data, dob_col='dob')
        data = standardisation_functions.standardise_names(data, name_cols=['first_name', 'surname'])
        data = standardisation_functions.fix_zero_length_strings(data)

        response = score(data)
        event_logger(__name__).info(f"PiCPersonMatchScoreGenerated", extra={
            'custom_dimensions': custom_dimensions_from(response)
        })
        return response
    except Exception as e:
        logger(__name__).exception('Exception at match endpoint')
        return e.args[0], 500


def custom_dimensions_from(response: dict):
    return {key: value['0'] for key, value in response.items() if
            key in [
                'unique_id_l',
                'unique_id_3',
                'pnc_number_std_l',
                'pnc_number_std_r',
                'source_dataset_l',
                'source_dataset_r',
                'match_probability'
            ]}


def score(data):
    with get_db() as conn:
        cursor = conn.cursor()

        # Register SQL functions
        # TODO register functions once on startup
        conn.create_function("concat", -1, sql_functions.concat)
        conn.create_function("jaro_winkler_sim", 2, jaro_winkler)
        conn.create_function("Dmetaphone", 1, sql_functions.Dmetaphone)
        conn.create_function("levenshtein", 2, levenshtein)
        conn.create_function("datediff", 2, sql_functions.datediff)

        # TODO create unique database tables
        data.to_sql(name='df', con=conn, if_exists='replace', index=False)
        cursor.execute(f"""CREATE TABLE df_comparison AS {model.df_comparison}""")
        cursor.execute(f"""CREATE TABLE df_with_gamma AS {model.df_with_gamma}""")
        cursor.execute(f"""CREATE TABLE df_with_gamma_probs AS {model.df_with_gamma_probs}""")
        cursor.execute(f"""CREATE TABLE df_e AS {model.df_e}""")

        json_output = pandas.read_sql("""select * from df_e""", con=conn).to_json()

        # TODO clean up database tables reliably
        cursor.execute("DROP TABLE IF EXISTS df_comparison")
        cursor.execute("DROP TABLE IF EXISTS df_with_gamma")
        cursor.execute("DROP TABLE IF EXISTS df_with_gamma_probs")
        cursor.execute("DROP TABLE IF EXISTS df_e")

        return json.loads(json_output)


class UnsupportedError(Exception):
    fmt = 'unsupported request'
