import os
from pathlib import Path

current_dir = Path(__file__).parent

def getenv(key, default=None, func=None):
    """Get environment variable return None if non exits
    Args:
        key: key os environment
        default: default value if not exists
        func: apply function in env
    """
    val = os.getenv(key, default)
    if func:
        val = func(val)
    return val

class SoccerConfig(object):
    """Soccer Configuration"""
    # flask debug configuration
    DEBUG = getenv("DEBUG", False, bool)

    # static url for access assets
    STORAGE_PATH = getenv("STORAGE_PATH", "/var/www/html/file")

    # database config
    MYSQL_HOST = getenv("DB_HOST", "127.0.0.1")
    MYSQL_USER = getenv("DB_USER", "root")
    MYSQL_PASS = getenv("DB_PASS", "")
    MYSQL_DBNAME = getenv("DB_NAME", "cermin")
    MYSQL_PORT = getenv("DB_PORT", 3306, int)

    INTERNAL_TOKEN = "bnsultjhbqyydugtjvchrioszozwxmlpcocdmjdv"

    # sqlalchemy
    # mysql://username:password@server:port/db
    SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s:%s/%s?charset=utf8mb4" % (
        MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DBNAME
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = getenv("SQLALCHEMY_TRACK_MODIFICATIONS", False, bool)
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_RECYCLE = 60
    SQLALCHEMY_MAX_OVERFLOW = 20

    # token secret key
    SECRET_KEY = getenv("SECRET_KEY", "soccerappnyoba")

    # max file upload 100mb
    MAX_CONTENT_LENGTH = getenv("MAX_CONTENT_LENGTH", 100 * 1024 * 1024, int)

    # WEB frontend configuration
    WEB_URL = getenv("WEB_URL", "http://localhost:5000")

    # endpoint scope authorization
    ROLE_SCOPE = {
        "user": [
            "user",
            "pertandingan",
        ],
        "administrator": [
            "administrator",
            "dashboard",
            "user",
            "pertandingan",
        ]
    }

    # Konfigurasi logging yang menampilkan log level INFO (INFO, ERROR, WARNING)
    # Console:
    #
    # output: "INFO 2016-01-05 15:38:55,126 - soccer.route.v1.error - error.py:12: error authentifikasi"
    LOG_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "[%(levelname)s] %(asctime)s - %(name)s - %(filename)s:%(lineno)d: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": getenv("LOG_LEVEL", 'INFO'),
                "formatter": "verbose",
                "stream": "ext://sys.stdout"
            }
        },
        "loggers":{
            "*": {
                "propagate": False,
                "handlers": ["console"]
            }
        },
        "root": {
            "level": getenv("LOG_LEVEL", "INFO"),
            "handlers": [
                "console"
            ]
        }
    }