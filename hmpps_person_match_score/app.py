import logging

from flask import Flask
from views.health_view import HealthView
from views.match_view import MatchView
from views.ping_view import PingView

from hmpps_person_match_score.app_insights import AppInsightsLogger


class MatchScoreFlaskApplication:
    """
    Match Score Flask Application
    """

    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.initialise()

    def initialise(self):
        """
        Initialise application
        """
        self.initialise_logger()
        self.initialise_request_handlers()
        
    def initialise_request_handlers(self):
        """
        Set up request handlers, passes logger to each view
        Each request handler can define ROUTE const as url rule
        """
        for request_handler in [
            PingView,
            HealthView, 
            MatchView
        ]:
            self.app.add_url_rule(request_handler.ROUTE, view_func=request_handler.as_view(
                request_handler.__name__, self.logger, self.event_logger))

    def initialise_logger(self):
        """
        Set up application logger
        """
        logging.basicConfig(level=logging.INFO)
        # self.wsgi_app = app_insights_logger().initRequestMiddleware(self.wsgi_app)
        logger_instance = AppInsightsLogger.instance()
        self.logger = logger_instance.get_logger(__name__)
        self.event_logger = logger_instance.get_event_logger(__name__)

    def run(self):
        """
        Run the Application
        """
        self.app.run()

if __name__ == "__main__":
    MatchScoreFlaskApplication().run()
