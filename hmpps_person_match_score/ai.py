import logging
import os

from opencensus.ext.azure.log_exporter import AzureLogHandler

from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace.samplers import ProbabilitySampler


def role_name_processor(envelope):
    envelope.tags['ai.cloud.role'] = 'hmpps-person-match-score'

class AILogger:
    _use_ai = True
    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            try:
                logger = cls._instance.get_logger(__name__)
            except ValueError as e:
                assert e.args[0] == 'Instrumentation key cannot be none or empty.'
                cls._use_ai = False
                logger = cls._instance.get_logger(__name__)
                logger.warning("Logs will not post to AppInsights as no instrumentation key has been provided")
        return cls._instance

    def get_logger(self, name):
        logger = logging.getLogger(__name__)
        if self._use_ai:
            handler = AzureLogHandler()
            handler.add_telemetry_processor(role_name_processor)
            logger.addHandler(handler)
        return logger

    def initRequestMiddleware(self, app):
        if self._use_ai:
            exporter = AzureExporter()
            exporter.add_telemetry_processor(role_name_processor)
            middleware = FlaskMiddleware(
                app,
                exporter=exporter,
                sampler=ProbabilitySampler(rate=1.0)
            )

instance = AILogger.instance()
