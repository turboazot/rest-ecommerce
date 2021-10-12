from flask_sqlalchemy import SQLAlchemy, BaseQuery, Model, SignallingSession, _include_sqlalchemy, utils, _SQLAlchemyState
from sqlalchemy.ext.horizontal_shard import ShardedSession
from sqlalchemy import orm, sql, util
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.session import attributes, context
from sqlalchemy.sql.selectable import LABEL_STYLE_TABLENAME_PLUS_COL
import flask_marshmallow
import re
from threading import Lock
import mmh3
from functools import reduce
try:
    from greenlet import getcurrent as _ident_func
except ImportError:
    try:
        from threading import get_ident as _ident_func
    except ImportError:
        # Python 2.7
        from thread import get_ident as _ident_func
from sqlalchemy.pool import StaticPool, NullPool
import sqlalchemy

class BindKeyPattern:
    def __init__(self, pattern):
        self.pattern = re.compile(pattern)

    def __eq__(self, other):
        try:
            return self.pattern.match(other)
        except TypeError:
            return NotImplemented

# class ShardedQuery(BaseQuery):
#     partition_key = None
#     def count(self):
#         col = sql.func.count(sql.literal_column("*"))
#         count = self._from_self(col).enable_eagerloads(False).all()
#         return reduce((lambda x, y: x[0]+y[0]), count)

class ShardedPrimaryKeySession(ShardedSession):
    def _get_impl(
        self,
        entity,
        primary_key_identity,
        db_load_fn,
        options=None,
        populate_existing=False,
        with_for_update=None,
        identity_token=None,
        execution_options=None,
    ):

        # convert composite types to individual args
        if hasattr(primary_key_identity, "__composite_values__"):
            primary_key_identity = primary_key_identity.__composite_values__()

        mapper = inspect(entity)

        is_dict = isinstance(primary_key_identity, dict)
        # if not is_dict:
        #     primary_key_identity = util.to_list(
        #         primary_key_identity, default=(None,)
        #     )

        # if len(primary_key_identity) != len(mapper.primary_key):
        #     raise sa_exc.InvalidRequestError(
        #         "Incorrect number of values in identifier to formulate "
        #         "primary key for query.get(); primary key columns are %s"
        #         % ",".join("'%s'" % c for c in mapper.primary_key)
        #     )

        # if is_dict:
        #     try:
        #         primary_key_identity = list(
        #             primary_key_identity[prop.key]
        #             for prop in mapper._identity_key_props
        #         )

        #     except KeyError as err:
        #         util.raise_(
        #             sa_exc.InvalidRequestError(
        #                 "Incorrect names of values in identifier to formulate "
        #                 "primary key for query.get(); primary key attribute "
        #                 "names are %s"
        #                 % ",".join(
        #                     "'%s'" % prop.key
        #                     for prop in mapper._identity_key_props
        #                 )
        #             ),
        #             replace_context=err,
        #         )

        if (
            not populate_existing
            and not mapper.always_refresh
            and with_for_update is None
        ):

            instance = self._identity_lookup(
                mapper, primary_key_identity, identity_token=identity_token
            )

            if instance is not None:
                # reject calls for id in identity map but class
                # mismatch.
                if not issubclass(instance.__class__, mapper.class_):
                    return None
                return instance
            elif instance is attributes.PASSIVE_CLASS_MISMATCH:
                return None

        # set_label_style() not strictly necessary, however this will ensure
        # that tablename_colname style is used which at the moment is
        # asserted in a lot of unit tests :)

        load_options = context.QueryContext.default_load_options

        if populate_existing:
            load_options += {"_populate_existing": populate_existing}
        statement = sql.select(mapper).set_label_style(
            LABEL_STYLE_TABLENAME_PLUS_COL
        )
        if with_for_update is not None:
            statement._for_update_arg = query.ForUpdateArg._from_argument(
                with_for_update
            )

        if options:
            statement = statement.options(*options)
        if execution_options:
            statement = statement.execution_options(**execution_options)
        
        primary_key_identity = util.to_list(
            primary_key_identity["id"], default=(None,)
        )
        
        return db_load_fn(
            self,
            statement,
            primary_key_identity,
            load_options=load_options,
        )

class ShardedSQLAlchemy(SQLAlchemy):

    def __init__(self, app=None, use_native_unicode=True, session_options=None,
                 metadata=None, query_class=BaseQuery, model_class=Model,
                 engine_options=None):

        self.use_native_unicode = use_native_unicode
        self.Query = query_class
        self.default_session = self.create_scoped_default_session(session_options)
        self.Model = self.make_declarative_base(model_class, metadata)
        self._engine_lock = Lock()
        self.app = app
        self._engine_options = engine_options or {}
        _include_sqlalchemy(self, query_class)

        if app is not None:
            self.init_app(app)
    
    def init_app(self, app, sharded_session_options=None):
        if (
            'SQLALCHEMY_DATABASE_URI' not in app.config and
            'SQLALCHEMY_BINDS' not in app.config
        ):
            warnings.warn(
                'Neither SQLALCHEMY_DATABASE_URI nor SQLALCHEMY_BINDS is set. '
                'Defaulting SQLALCHEMY_DATABASE_URI to "sqlite:///:memory:".'
            )

        app.config.setdefault('SQLALCHEMY_DATABASE_URI', 'sqlite:///:memory:')
        app.config.setdefault('SQLALCHEMY_BINDS', None)
        app.config.setdefault('SQLALCHEMY_NATIVE_UNICODE', None)
        app.config.setdefault('SQLALCHEMY_ECHO', False)
        app.config.setdefault('SQLALCHEMY_RECORD_QUERIES', None)
        app.config.setdefault('SQLALCHEMY_POOL_SIZE', None)
        app.config.setdefault('SQLALCHEMY_POOL_TIMEOUT', None)
        app.config.setdefault('SQLALCHEMY_POOL_RECYCLE', None)
        app.config.setdefault('SQLALCHEMY_MAX_OVERFLOW', None)
        app.config.setdefault('SQLALCHEMY_COMMIT_ON_TEARDOWN', False)
        track_modifications = app.config.setdefault(
            'SQLALCHEMY_TRACK_MODIFICATIONS', None
        )
        app.config.setdefault('SQLALCHEMY_ENGINE_OPTIONS', {})

        if track_modifications is None:
            warnings.warn(FSADeprecationWarning(
                'SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and '
                'will be disabled by default in the future.  Set it to True '
                'or False to suppress this warning.'
            ))

        # Deprecation warnings for config keys that should be replaced by SQLALCHEMY_ENGINE_OPTIONS.
        utils.engine_config_warning(app.config, '3.0', 'SQLALCHEMY_POOL_SIZE', 'pool_size')
        utils.engine_config_warning(app.config, '3.0', 'SQLALCHEMY_POOL_TIMEOUT', 'pool_timeout')
        utils.engine_config_warning(app.config, '3.0', 'SQLALCHEMY_POOL_RECYCLE', 'pool_recycle')
        utils.engine_config_warning(app.config, '3.0', 'SQLALCHEMY_MAX_OVERFLOW', 'max_overflow')

        app.extensions['sqlalchemy'] = _SQLAlchemyState(self)

        self.app = app

        # Create sharded session object
        self.session = self.create_scoped_session(sharded_session_options)

        @app.teardown_appcontext
        def shutdown_session(response_or_exc):
            if app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']:
                warnings.warn(
                    "'COMMIT_ON_TEARDOWN' is deprecated and will be"
                    " removed in version 3.1. Call"
                    " 'db.session.commit()'` directly instead.",
                    DeprecationWarning,
                )

                if response_or_exc is None:
                    self.session.commit()

            self.session.remove()
            return response_or_exc
    
    def _get_shard_by_partition_key(self, partition_key):
        app = self.get_app()
        binds = app.config["SQLALCHEMY_BINDS"]
        shard_keys = sorted(binds.keys())
        hash_value = mmh3.hash(str(partition_key)) + 2147483648
        if hash_value >=0 and hash_value < 2147483648:
            return shard_keys[0]
        elif hash_value >= 2147483648 and hash_value < 4294967296:
            return shard_keys[1]
        raise Exception(f"Hash value {hash_value} is invalid")

    def _shard_chooser(self, mapper, instance, clause=None):
        if instance:
            app = self.get_app()
            binds = app.config["SQLALCHEMY_BINDS"]
            bind_key = instance.__bind_key__
            matched_binds = {k: v for k, v in binds.items() if k == bind_key}
            shard_keys = sorted(matched_binds.keys())
            _, ident, _ = mapper.identity_key_from_instance(instance)
            partition_key = instance.id["partition_key"]
            instance.id = instance.id["id"]
            return self._get_shard_by_partition_key(partition_key)
            

    def _id_chooser(self, query, ident):
        app = self.get_app()
        binds = app.config["SQLALCHEMY_BINDS"]
        r = [self._get_shard_by_partition_key(ident["partition_key"])]
        # r = sorted(binds.keys())
        return r
    
    def _execute_chooser(self, query):
        app = self.get_app()
        binds = app.config["SQLALCHEMY_BINDS"]
        return sorted(binds)

    def create_scoped_default_session(self, options=None):
        if options is None:
            options = {}

        scopefunc = options.pop('scopefunc', _ident_func)
        options.setdefault('query_cls', self.Query)
        return orm.scoped_session(
            self.create_default_session(options), scopefunc=scopefunc
        )

    def create_default_session(self, options):
        return orm.sessionmaker(class_=SignallingSession, db=self, expire_on_commit=False, **options)

    def create_session(self, options):
        """Override.
        """
        app = self.get_app()
        binds = app.config["SQLALCHEMY_BINDS"]
        shards = {}
        for key in binds.keys():
            shards[key] = self.get_engine(app, key)
        options = options.copy()
        options.update({
            'shards': shards,
            'shard_chooser': self._shard_chooser,
            'id_chooser': self._id_chooser,
            'query_chooser': self._execute_chooser
        })
        return orm.sessionmaker(class_=ShardedPrimaryKeySession, expire_on_commit=False, **options)


ma = flask_marshmallow.Marshmallow()
db = ShardedSQLAlchemy()