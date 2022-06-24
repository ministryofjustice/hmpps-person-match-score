from flask import current_app, g as app_context
import splink.model


def get_model():
    if 'model' not in app_context:
        app_context.model = splink.model.load_model_from_json(current_app.config['MODEL'])

    return app_context.model
