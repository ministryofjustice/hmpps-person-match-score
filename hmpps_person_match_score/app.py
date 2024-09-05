import logging
import os
import platform
import sys
import tracemalloc

import duckdb

# Must be imported before flask
from azure.monitor.opentelemetry import configure_azure_monitor

from hmpps_person_match_score.log_formatter import LogFormatter

# required to be able to log result code to appinsights
if os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING"):
    os.environ["OTEL_SERVICE_NAME"] = "hmpps-person-match-score"
    configure_azure_monitor(logger_name="hmpps-person-match-score-logger")

import flask

from hmpps_person_match_score.views.health_view import HealthView
from hmpps_person_match_score.views.info_view import InfoView
from hmpps_person_match_score.views.match_view import MatchView
from hmpps_person_match_score.views.person_match_view import PersonMatchView

tracemalloc.start()

s = None

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
        self.log_version()
        self.initiaise_duckdb_connection()
        self.initialise_request_handlers()

    def log_version(self):
        """
        Log application version
        """
        version = " ".join(sys.version.split(" ")[:1])
        log_message = f"Starting hmpps-person-match-score using Python {version} on {platform.platform()}"
        self.logger.info(log_message)

    def mem_snapshot(self):
        global s  # noqa: PLW0603
        if not s:
            s = tracemalloc.take_snapshot()
            return "Taken snapshot\n"
        else:
            lines = []
            top_stats = tracemalloc.take_snapshot().compare_to(s, "lineno")
            for stat in top_stats[:5]:
                lines.append(str(stat))
            return "\n".join(lines)

    def initialise_request_handlers(self):
        """
        Set up request handlers, passes logger to each view
        Each request handler can define ROUTE const as url rule
        """
        for request_handler in [HealthView, MatchView, InfoView, PersonMatchView]:
            self.app.add_url_rule(
                request_handler.ROUTE,
                view_func=request_handler.as_view(request_handler.__name__, self.logger, self.duckdb_connection),
            )
        self.app.add_url_rule("/snapshot", view_func=self.mem_snapshot)

    def initiaise_duckdb_connection(self):
        """
        Set up duckdb database connection
        """
        self.duckdb_connection = duckdb.connect(database=":memory:")
        self.duckdb_connection.execute("SET temp_directory='/tmp/duckdb/';")

    def initialise_logger(self):
        """
        Set up application logger
        """
        # this suppresses app insights logs from stdout
        logging.Formatter = LogFormatter
        logging.basicConfig(
            level=logging.WARNING,
            format="%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.logger = logging.getLogger(self.LOGGER_NAME)
        self.logger.setLevel(logging.INFO)

    def run(self):
        """
        Run the Application
        """
        self.app.run()


if __name__ == "__main__":
    MatchScoreFlaskApplication().run()
