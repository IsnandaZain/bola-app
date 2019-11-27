import logging

from flask import Blueprint, jsonify
from itsdangerous import BadSignature

from soccer.exceptions import SoccerException
from soccer.models import db

__author__ = "isnanda.muhammadzain@sebangsa.com"

bp = Blueprint(__name__, "error")
logger = logging.getLogger(__name__)


@bp.app_errorhandler(BadSignature)
def handle_bad_signature(e):
    """Will be execute if access_token broken by ``raise BadSignature``
    ::

        {
            "status": 401,
            "message": "Your token signature is broken please
            check your token or request new token"
        }
    """
    logger.error(e)

    tampil = {
        "status": 401,
        "message": 
            ("Your token signature is broken, "
             "please check your token or request new token")
    }

    return jsonify(tampil), 401


@bp.app_errorhandler(SoccerException)
def handle_invalid_usage(e):
    """Will be execute if SoccerException or child raised

    just sample result, code and message event payload must be different::

        {
            "message": "User not found"
        }
    """
    logger.warning(e.message)
    db.session.rollback()
    return jsonify(e.to_dict()), e.status_code


@bp.app_errorhandler(404)
def page_not_found(e):
    """404 endpoint not found
    ::

        {
            "status": 404,
            "message": "Sorry page not exists"
        }
    """
    logger.warning(e)
    tampil = {"status": 404, "message": "Sorry page not exists"}
    return jsonify(tampil), 404


@bp.app_errorhandler(405)
def method_not_allowed(e):
    """405 method now allowed
    ::

        {
            "status": 405,
            "message": "Method not allowed"
        }
    """
    logger.warning(e)
    tampil = {"status": 405, "message": "Method not allowed"}
    return jsonify(tampil), 405


@bp.app_errorhandler(500)
def server_error(e):
    """500 service is broken
    ::

        {
            "status": 500,
            "message": "Uhandled exception occured, 
            please contact API division :)"
        }
    """
    logger.error(e)
    message = "Uhandled exception occured, please contact API division :)"

    tampil = {
        "status": 500,
        "message": message
    }
    return jsonify(tampil), 500


@bp.route("/errorz")
def trigger_error():
    raise ValueError("error triggered")