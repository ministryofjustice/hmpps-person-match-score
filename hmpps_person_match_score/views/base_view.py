import os
import uuid
from typing import List

import flask
from flask.views import MethodView
from pydantic import BaseModel, ValidationError
from werkzeug.exceptions import BadRequest

from hmpps_person_match_score.domain.splink_models import SplinkModels


class BaseView(MethodView):
    """
    Base View Class to initialise logger
    Include request as part of the object
    """

    def __init__(self, logger, duckdb_connection) -> None:
        super().__init__()
        self.logger = logger
        self.duckdb_connection = duckdb_connection
        self.request = flask.request

    def validate(self, model: BaseModel):
        """
        validate incoming message
        """
        try:
            return model(**self.request.json)
        except ValidationError as err:
            raise BadRequest("Message in incorrect format") from err

    @staticmethod
    def get_model_path(model: SplinkModels):
        """
        Get model path from environment variable
        """
        model_path = f"./hmpps_person_match_score/splink_models/{model.value}.json"
        if not os.path.exists(model_path):
            raise Exception(f"{model_path} does not exist.")
        return model_path

    @staticmethod
    def generate_view_uuid():
        return f"v_{uuid.uuid4().hex.replace('-', '')[:16]}"

    def cleanup_splink_tables(self, linker, input_table_alias: List[str]):
        """
        Cleans up intermediate tables created by Splink in the DuckDB connection
        """
        table_prefixes = ("__splink__df_concat_with_tf_", "__splink__df_predict_")

        for k, v in list(linker._intermediate_table_cache.items()):  # noqa: SLF001
            if k.startswith(table_prefixes):
                v.drop_table_from_database_and_remove_from_cache()

        for alias in input_table_alias:
            self.duckdb_connection.sql(f"DROP VIEW IF EXISTS {alias}")
