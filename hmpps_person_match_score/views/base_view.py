import os

import flask
from flask.views import MethodView
from pydantic import BaseModel, ValidationError
from werkzeug.exceptions import BadRequest


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
    def get_model_path():
        """
        Get model path from environment variable
        """
        model_path = os.environ.get("MODEL_PATH", "./hmpps_person_match_score/model.json")
        if not os.path.exists(model_path):
            raise Exception(f"MODEL_PATH {model_path} does not exist.")
        return model_path
