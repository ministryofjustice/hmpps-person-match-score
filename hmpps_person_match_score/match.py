import json
import flask
import pandas as pd
from splink.duckdb.duckdb_linker import DuckDBLinker
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
    return 'Healthy: No db check to be completed'


@blueprint.route('/match', methods=['POST'])
def match():
    try:
        logger(__name__).info("Match score requested")
        
        # data = pd.read_json(json.dumps(flask.request.get_json()), dtype=str)
        # This no longer works with the test data (I think as of Python 3.x), try this instead:
        data = pd.DataFrame(json.loads(flask.request.get_data().decode('utf-8')))
       
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
    # Set up DuckDB linker
    linker = DuckDBLinker(
        [data[data['source_dataset'] == data['source_dataset'].unique()[0]], 
         data[data['source_dataset'] == data['source_dataset'].unique()[1]]],
        input_table_aliases=[data['source_dataset'].unique()[0], data['source_dataset'].unique()[1]]
    )
    linker.load_settings_from_json('./hmpps_person_match_score/model.json')        
    
    # Make predictions
    json_output = linker.predict().as_pandas_dataframe().to_json()
    
    # Return
    return json.loads(json_output)


class UnsupportedError(Exception):
    fmt = 'unsupported request'
