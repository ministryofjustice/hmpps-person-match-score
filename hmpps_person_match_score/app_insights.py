import logging
import os

from opencensus.ext.azure.log_exporter import AzureEventHandler, AzureLogHandler
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace.samplers import ProbabilitySampler


class AppInsightsLogger:
    """
    Appinsight logger
    """

    _use_ai = True

    def __init__(self, app):
        self.logger = logging.getLogger()
        self.has_instrumentation_key()
        self.add_azure_event_handler()
        self.add_azure_log_handler()
        self.init_request_middleware(app)

    @staticmethod
    def role_name_processor(envelope):
        envelope.tags["ai.cloud.role"] = "hmpps-person-match-score"

    def has_instrumentation_key(self):
        """
        Verify connection string is set
        """
        if not os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING"):
            self._use_ai = False
            self.logger.warning("Logs will not post to AppInsights as no instrumentation key has been provided")

    def add_azure_log_handler(self):
        if self._use_ai:
            handler = AzureLogHandler()
            handler.add_telemetry_processor(self.role_name_processor)
            self.logger.addHandler(handler)

    def add_azure_event_handler(self):
        if self._use_ai:
            handler = AzureEventHandler()
            handler.add_telemetry_processor(self.role_name_processor)
            self.logger.addHandler(handler)

    def init_request_middleware(self, app):
        if self._use_ai:
            exporter = AzureExporter()
            exporter.add_telemetry_processor(self.role_name_processor)
            FlaskMiddleware(
                app, exporter=exporter, sampler=ProbabilitySampler(rate=1.0))
