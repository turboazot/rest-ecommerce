import flask
import flask_restx

import api.config
import api.routes.v1.products
import api.routes.v1.users


def get_blueprint():
    v1_bp = flask.Blueprint(api.config.Config.V1_PREFIX,
                            __name__,
                            url_prefix=api.config.Config.V1_PREFIX)

    v1_routes = flask_restx.Api(v1_bp,
                                title='Rest API v1',
                                version='1',
                                description='Rest API v1')

    v1_routes.add_namespace(api.routes.v1.products.products_ns)
    v1_routes.add_namespace(api.routes.v1.users.users_ns)

    return v1_bp
