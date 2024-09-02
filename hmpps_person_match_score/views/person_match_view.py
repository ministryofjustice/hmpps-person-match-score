import json

import pyarrow as pa
from splink.duckdb.duckdb_linker import DuckDBLinker

from hmpps_person_match_score.domain.events import Events
from hmpps_person_match_score.domain.splink_models import SplinkModels
from hmpps_person_match_score.models.person_match_model import PersonMatching
from hmpps_person_match_score.views.base_view import BaseView


class PersonMatchView(BaseView):
    """
    Match View
    """

    ROUTE = "/person/match"

    SCHEMA = pa.schema(
        [
            pa.field("unique_id", pa.string(), nullable=True),
            pa.field("source_dataset", pa.string(), nullable=False),
            pa.field("pnc", pa.string(), nullable=True),
            pa.field("dob", pa.string(), nullable=True),
            pa.field("lastname", pa.string(), nullable=True),
            pa.field("firstname1", pa.string(), nullable=True),
            pa.field("firstname2", pa.string(), nullable=True),
            pa.field("firstname3", pa.string(), nullable=True),
        ],
    )

    def post(self):
        """
        POST request handler
        """
        self.logger.info(Events.PERSON_MATCH_SCORE_REQUESTED)
        person_match_model = self.validate(model=PersonMatching)
        result = self.match(person_match_model)
        self.logger.info(
            Events.PERSON_MATCH_SCORE_GENERATED,
            extra={"custom_dimensions": json.dumps(result.get("match_probability"))},
        )
        return result

    def match(self, person_match_model: PersonMatching):
        """
        Match records
        """
        pmm_dict = person_match_model.model_dump()
        dataset_1 = pa.Table.from_pylist(pmm_dict["matching_to"], schema=self.SCHEMA)
        dataset_2 = pa.Table.from_pylist([pmm_dict["matching_from"]], schema=self.SCHEMA)
        linker = DuckDBLinker(
            [dataset_1, dataset_2],
            connection=self.duckdb_connection,
        )
        linker.load_settings(self.get_model_path(SplinkModels.PERSON_MATCH_MODEL))

        prediction = linker.predict()

        json_output = prediction.as_pandas_dataframe().to_json()

        # Clean up prediction table from database
        linker._delete_table_from_database(prediction.physical_name)

        return json.loads(json_output)
