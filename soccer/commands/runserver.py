import click
from werkzeug.contrib.profiler import ProfileMiddleware

from soccer import http
from configuration import SoccerConfig

__author__ = "isnanda.muhammadzain@sebangsa.com"


LOG_DEBUG = SoccerConfig.LOG_CONFIG
LOG_DEBUG["handlers"]["console"]["level"] = "DEBUG"


class SoccerConfigDebug(SoccerConfig):
    """flask debug configuration"""

    # Debugging mode
    DEBUG = True

    # prettify json
    JSONIFY_PRETTYPRINT_REGULAR = True

    LOG_CONFIG = LOG_DEBUG


@click.command()
@click.option("--port", help="runserver port")
@click.option("--debug", is_flag=True, help="runserver with debug mode")
@click.option("--profiling", is_flag=True, help="add profiling middleware")
def runserver(port, debug, profiling):
    """runserver flask"""
    if port: 
        port = int(port)
    else:
        port = 5000

    if debug:
        app_instance = http.factory(config=SoccerConfigDebug)
    else:
        app_instance = http.factory()

    if profiling:
        app_instance.config["PROFILE"] = True
        app_instance.wsgi_app = ProfileMiddleware(
            app_instance.wsgi_app, restrictions=[30]
        )

    app_instance.run(host="0.0.0.0", port=port, debug=True)