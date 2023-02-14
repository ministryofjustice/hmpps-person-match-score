import os
import platform
import sys
from logging.config import dictConfig

import flask
from . import match, ai

def create_app(test_config=None):
    ai_logger_instance = ai.instance
    try:
        ai_logger_instance.get_logger(__name__).info("Starting hmpps-person-match-score using Python %s on %s" % (" ".join(sys.version.split(" ")[:1]), platform.platform()))

        dictConfig({
            'version': 1,
            'formatters': {'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            }},
            'handlers': {'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default'
            }},
            'root': {
                'level': 'INFO',
                'handlers': ['wsgi']
            }
        })


        # create and configure the app
        app = flask.Flask(__name__, instance_relative_config=True)
        ai_logger_instance.initRequestMiddleware(app)

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
    except Exception as e:
        ai_logger_instance.get_logger(__name__).exception('Exception on start up')


