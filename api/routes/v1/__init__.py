import flask
import flask_restx

import api.config
import api.routes.v1.services


def get_blueprint():
    v1_bp = flask.Blueprint(api.config.Config.V1_PREFIX,
                            __name__,
                            url_prefix=api.config.Config.V1_PREFIX)

    v1_routes = flask_restx.Api(v1_bp,
                                title='Rest API v1',
                                version='1',
                                description='Rest API v1')

    v1_routes.add_namespace(api.routes.v1.services.services_ns)

    return v1_bp
