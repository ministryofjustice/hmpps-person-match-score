import os

import duckdb
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

    def __init__(self, logger) -> None:
        super().__init__()
        self.duckdb_connection = duckdb.connect(database=":memory:")
        self.logger = logger
        self.request = flask.request

    def __del__(self):
        self.duckdb_connection.close()

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
