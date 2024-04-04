import flask
from flask.views import MethodView


class BaseView(MethodView):
    """
    Base View Class to initialise logger
    Include request as part of the object
    """

    def __init__(self, logger) -> None:
        super().__init__()
        self.logger = logger
        self.request = flask.request
