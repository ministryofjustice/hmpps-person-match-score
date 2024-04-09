import logging
import os
import platform
import sys

import flask
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry.instrumentation.flask import FlaskInstrumentor

from hmpps_person_match_score.views.health_view import HealthView
from hmpps_person_match_score.views.info_view import InfoView
from hmpps_person_match_score.views.match_view import MatchView
from hmpps_person_match_score.views.ping_view import PingView


class MatchScoreFlaskApplication:
    """
    Match Score Flask Application
    """

    APPLICATION_NAME = "hmpps-person-match-score"
    LOGGER_NAME = "hmpps-person-match-score-logger"

    def __init__(self) -> None:
        self.app = flask.Flask(self.APPLICATION_NAME)
        self.wsgi_app = self.app.wsgi_app
        self.initialise()

    def initialise(self):
        """
        Initialise application
        """
        self.initialise_logger()
        self.configure_app_insights()
        self.log_version()
        self.initialise_request_handlers()

    def log_version(self):
        """
        Log application version
        """
        version = " ".join(sys.version.split(" ")[:1])
        log_message = f"Starting hmpps-person-match-score using Python {version} on {platform.platform()}"
        self.logger.info(log_message)

    def initialise_request_handlers(self):
        """
        Set up request handlers, passes logger to each view
        Each request handler can define ROUTE const as url rule
        """
        for request_handler in [PingView, HealthView, MatchView, InfoView]:
            self.app.add_url_rule(
                request_handler.ROUTE,
                view_func=request_handler.as_view(request_handler.__name__, self.logger),
            )

    def initialise_logger(self):
        """
        Set up application logger
        """
        self.logger = logging.getLogger(self.LOGGER_NAME)
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)-8s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.logger = logging.getLogger(self.LOGGER_NAME)

    def configure_app_insights(self):
        """
        Set up appinsights
        """
        if os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING"):
            os.environ["OTEL_SERVICE_NAME"] = "hmpps-person-match-score"
            configure_azure_monitor(
                instrumentation_options={
                    "flask": {"enabled": True},
                    "azure_sdk": {"enabled": True},
                },
                logger_name=self.LOGGER_NAME,
            )
            FlaskInstrumentor().instrument_app(self.app)
        else:
            self.logger.warning("Logs will not post to AppInsights as no instrumentation key has been provided")

    def run(self):
        """
        Run the Application
        """
        self.app.run()


if __name__ == "__main__":
    MatchScoreFlaskApplication().run()
