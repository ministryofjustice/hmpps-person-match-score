import json
import flask
import pandas as pd
from splink.duckdb.duckdb_linker import DuckDBLinker
from . import standardisation_functions
from . import ai

blueprint = flask.Blueprint('match', __name__)

logger = ai.instance.get_logger(__name__)

@blueprint.route('/ping', methods=['GET'])
def ping():
    try:
        return "pong"
    except Exception as e:
        logger.exception('Exception at ping endpoint')
        return e.args[0], 500
    
@blueprint.route('/health', methods=['GET'])
def health():
    return 'Healthy: No db check to be completed'


@blueprint.route('/match', methods=['POST'])
def match():
    try:
        logger.info("Match score requested")
        data = pd.read_json(json.dumps(flask.request.get_json()), dtype=str)

        data = standardisation_functions.standardise_pnc_number(data, pnc_col='pnc_number')
        data = standardisation_functions.standardise_dob(data, dob_col='dob')
        data = standardisation_functions.standardise_names(data, name_cols=['first_name', 'surname'])
        data = standardisation_functions.fix_zero_length_strings(data)

        response = score(data)
        logger.info("Match score completed")
        return response
    except Exception as e:
        logger.exception('Exception at match endpoint')
        return e.args[0], 500


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
