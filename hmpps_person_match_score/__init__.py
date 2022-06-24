import logging
import os
from logging.config import dictConfig
import flask
from . import spark, match
from pathlib import Path


def create_app(test_config=None):
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

    model = os.path.join(app.root_path, 'model', 'saved_model.json')

    # Spark jars that provide extended string comparison functions such as Jaro Winkler
    j = ['scala-udf-similarity-0.0.8.jar', 'graphframes-0.8.0-spark3.0-s_2.12.jar']
    jar_paths = [os.path.join(app.root_path, 'jars', jar) for jar in j]
    jars = ",".join(jar_paths)
    logging.info("Configuring jars: " + jars)

    app.config.from_mapping(
        SECRET_KEY='dev',
        MODEL=model,
        JARS=jars
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    app.register_blueprint(match.blueprint)

    # spark.init_app(app)

    return app
