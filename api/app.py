import flask
import flask_migrate
import api.config
import api.routes.v1
import api.extensions
import http
from logging.config import dictConfig


def create_app(config=api.config.Config):
    app = flask.Flask(__name__)
    app.config.from_object(config)

    dictConfig({
        'version': 1,
        'formatters': {
            'default': {
                'format':
                '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            }
        },
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default'
            }
        },
        'root': {
            'level': app.config['LOG_LEVEL']
        }
    })

    app.url_map.strict_slashes = False

    register_blueprints(app)
    register_extensions(app)

    return app


def register_blueprints(app):
    @app.route('/healthz')
    def healthz():
        return '{"status": "OK"}', http.HTTPStatus.OK

    app.register_blueprint(api.routes.v1.get_blueprint())


def register_extensions(app):
    api.extensions.ma.init_app(app)
    api.extensions.db.init_app(app)
    migrate = flask_migrate.Migrate(app, api.extensions.db)
