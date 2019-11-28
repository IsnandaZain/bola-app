# Events modules
# for send event and listen to event
# using signals and sqlalchemt event
import logging
import time

from MySQLdb.connections import Connection as MysqlConnection
from flask import g
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.pool import Pool

from soccer.models import db

log = logging.getLogger(__name__)


def register_event():
    pass


@event.listens_for(Pool, "connect")
def set_unicode(*args):
    connection = args[0]
    if isinstance(connection, MysqlConnection):
        cursor = connection.cursor()
        cursor.execute("SET NAMES 'utf8mb4' COLLATE 'utf8mb4_unicode_ci'")


@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(*args):
    """Logging engine execute"""
    conn = args[0]
    statement = args[2]
    parameters = args[3]
    conn.info.setdefault("query_start_time", []).append(time.time())

    log.debug("Start Query: %s", statement)
    log.debug("parameter: %r", parameters)


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(*args):
    """Logging engine after execute"""
    conn = args[0]
    total = time.time() - conn.info["query_start_time"].pop(-1)
    log.debug("Query Complete!")
    log.debug("Total Time: %f", total)
    g.total_query = getattr(g, "total_query", 0)
    g.total_query += 1

