import json
import flask
import pandas as pd
import pyarrow as pa
from splink.duckdb.duckdb_linker import DuckDBLinker
from . import standardisation_functions
from hmpps_person_match_score.app_insights import logger, event_logger
import os
blueprint = flask.Blueprint('match', __name__)
model_path = os.environ.get('MODEL_PATH', './hmpps_person_match_score/model.json')
if not os.path.exists(model_path):
    raise Exception(f"MODEL_PATH {model_path} does not exist.")

cleaned_data_schema = pa.schema(
    [
        pa.field("source_dataset", pa.string(), nullable=True),
        pa.field("unique_id", pa.string(), nullable=True),
        pa.field("pnc_number_std", pa.string(), nullable=True),
        pa.field("dob_std", pa.string(), nullable=True),
        pa.field("surname_std", pa.string(), nullable=True),
        pa.field("forename1_std", pa.string(), nullable=True),
        pa.field("forename2_std", pa.string(), nullable=True),
        pa.field("forename3_std", pa.string(), nullable=True),
        pa.field("forename4_std", pa.string(), nullable=True),
        pa.field("forename5_std", pa.string(), nullable=True),
    ]
)

@blueprint.route('/ping', methods=['GET'])
def ping():
    try:
        return "pong"
    except Exception as e:
        logger(__name__).exception('Exception at ping endpoint')
        return e.args[0], 500
    
@blueprint.route('/health', methods=['GET'])
def health():
    return 'UP'


@blueprint.route('/match', methods=['POST'])
def match():
    try:
        logger(__name__).info("Match score requested")
        
        data = pd.DataFrame(json.loads(flask.request.get_data().decode('utf-8')))
       
        data = standardisation_functions.standardise_pnc_number(data, pnc_col='pnc_number')
        data = standardisation_functions.standardise_dob(data, dob_col='dob')
        data = standardisation_functions.standardise_names(data, name_cols=['first_name', 'surname'])
        data = standardisation_functions.fix_zero_length_strings(data)
        
        # If no source dataset provided assume it's in the same format we expect, our algorithm does not need to know which record is which 
        # so this is just a formality
        if len(data['source_dataset']) == 0:
            data['source_dataset'] = pd.Series({'0': 'libra', '1':'delius'})
            data['source_dataset'] = data['source_dataset'].astype('str')
            
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
                'unique_id_r',
                'pnc_number_std_l',
                'pnc_number_std_r',
                'source_dataset_l',
                'source_dataset_r',
                'match_probability'
            ]}


def score(data):

    row_1 = data[data["source_dataset"] == data["source_dataset"].unique()[0]]
    row_2 = data[data["source_dataset"] == data["source_dataset"].unique()[1]]

    # Important to impose explicit schema - otherwise where a column contains only
    # None DuckDB will have no way of knowing it's a nullable string column
    row_arrow_1 = pa.Table.from_pandas(
        row_1, schema=cleaned_data_schema, preserve_index=False
    )
    row_arrow_2 = pa.Table.from_pandas(
        row_2, schema=cleaned_data_schema, preserve_index=False
    )
    
    # Set up DuckDB linker
    linker = DuckDBLinker(
        [row_arrow_1, row_arrow_2],
        input_table_aliases=[data['source_dataset'].unique()[0], data['source_dataset'].unique()[1]]
    )
    linker.load_settings_from_json(model_path)
    
    # Make predictions
    json_output = linker.predict().as_pandas_dataframe().to_json()
    
    # Return
    return json.loads(json_output)


class UnsupportedError(Exception):
    fmt = 'unsupported request'
