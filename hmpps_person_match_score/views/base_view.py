import flask
from flask.views import MethodView


class BaseView(MethodView):
    """
    Base View Class to initialise logger
    Include request as part of the object
    """
    
    def __init__(self, logger, event_logger) -> None:
        super().__init__()
        self.logger = logger
        self.event_logger = event_logger
        self.request = flask.request
