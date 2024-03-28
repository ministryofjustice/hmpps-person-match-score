import logging
import os
import platform
import sys

import flask

from hmpps_person_match_score.app_insights import app_insights_logger, logger

from . import match


def create_app(test_config=None):
    try:
        logging.basicConfig(level=logging.INFO)

        # create and configure the app
        app = flask.Flask(__name__, instance_relative_config=True)
        app_insights_logger().initRequestMiddleware(app)

        logger(__name__).info("Starting hmpps-person-match-score using Python %s on %s" % (" ".join(sys.version.split(" ")[:1]), platform.platform()))

        app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'hmpps_person_match_score.sqlite'),
        )

        if test_config is None:
            # load the instance config, if it exists, when not testing
            app.config.from_pyfile('config.py', silent=True)
        else:
            # load the test config if passed in
            app.config.from_mapping(test_config)

        # ensure the instance folder exists
        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass

        app.register_blueprint(match.blueprint)

        return app
    except Exception:
        app_insights_logger().get_logger(__name__).exception('Exception on start up')


