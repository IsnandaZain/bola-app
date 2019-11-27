import logging
import logging.config
import time

from flask import Flask, g, request, blueprints

from soccer import models, events, metrics
from soccer.exceptions.soccerexceptions import BadRequest
from soccer.libs import ratelimit
from soccer.libs.misc import walk_modules
from configuration import SoccerConfig

log = logging.getLogger(__name__)


def factory(config=SoccerConfig):
    app_instance = Flask(__name__.split(",")[0])
    app_instance.make_null_session()

    # Register blueprint
    for modules in walk_modules("soccer.routes"):
        for obj in vars(modules).values():
            if isinstance(obj, blueprints.Blueprint):
                app_instance.register_blueprint(obj)

    # load flask config
    app_instance.config.from_object(config)

    # load log config
    logging.config.dictConfig(config.LOG_CONFIG)

    # load database
    models.db.init_app(app_instance)

    # setup middleware
    metrics.setup_metrics(app_instance)

    @app_instance.before_request
    def before():
        log.debug("request args '%r'" % request.args)
        log.debug("request form '%r'" % request.form)
        log.debug("request headers '%r'" % request.headers)
        g.request_start_time = time.time()

        token = request.headers.get("Authorization")

        if token:
            if len(token.split()) == 2:
                schema = token.split()[0].lower()
                token = token.split()[1]

                if schema != "bearer":
                    raise BadRequest("Schema token tidak didukung")
            else:
                raise BadRequest("Schema token tidak didukung")

            user = UserTokens.validate(token)

            if user.is_suspend:
                raise SuspendUser(token)
        
        else:
            user = None

        g.user_auth = user

    @app_instance.after_request
    def after(response):
        try:
            # commit transaction
            models.db.session.commit()
        except Exception:
            models.db.session.rollback()
            raise

        resp = time.time() - g.request_start_time
        log.info("endpoint '%s' response time %.3f", request.url_rule, resp)

        log.info("total query %i", getattr(g, "total_query", 0))

        limit = ratelimit.get_view_rate_limit()
        if limit and limit.send_x_headers:
            h = response.headers
            h.add('X-RateLimit-Remaining', str(limit.remaining))
            h.add('X-RateLimit-Limit', str(limit.limit))
            h.add('X-RateLimit-Reset', str(limit.reset))
        return response

    # register sqlalchemy event
    events.register_event()

    return app_instance

app = factory()