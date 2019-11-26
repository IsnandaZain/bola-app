from flask import Blueprint, request, jsonify

from soccer.controllers import teamfavorite as teamfavorite_ctrl
from soccer.exceptions import BadRequest
from soccer.libs.ratelimit import ratelimit


bp = Blueprint(__name__, "team_favorite")


@bp.route("/team/favorite", methods=["POST"])
@ratelimit(300)
def team_favorite():
    """Favorite team

    **endpoint**

    .. sourcecode:: http

        POST /team/favorite

    **success response**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: text/javascript

        {
            "status": 200,
            "message": "favorite team success"
        }

    :form team_id: team yang akan difavoritkan
    """
    team_id = request.form.get("team_id")
    
    if not team_id:
        raise BadRequest("team_id tidak boleh kosong")

    favorite = teamfavorite_ctrl.set_favorite(auth.user.id, team_id)

    response = {
        "status": 200,
        "message": "Berhasil memfavorite team"
    }

    return jsonify(response)


@bp.route("/team/unfavorite", methods=["POST"])
@ratelimit(300)
def team_unfavorite():
    """Unfavorite user

    **endpoint**

    .. sourcecode:: http

        POST /user/unfavorite

    **success response**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: text/javascript

        {
            "status": 200,
            "message": "Unfavorite team success"
        }

    :form team_id: team yang akan di-unfavoritekan
    """
    team_id = request.form.get("team_id")
    if not team_id:
        raise BadRequest("team_id tidak boleh kosong")

    unfavorite = teamfavorite_ctrl.set_unfavorite(auth.user.id, team_id)

    response = {
        "status": 200,
        "message": "Berhasil unfavorite team"
    }

    return jsonify(response)


@bp.route("/team/favorite", methods=["GET"])
@ratelimit(600)
def team_list_favorite():
    """Get list favorite team

    **endpoint**

    .. sourcecode:: http

        GET /team/favorite

    **success response**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: text/javascript

        {
            "status": 200,
            "has_next": false,
            "has_prev": false,
            "result": [

            ]
        }

    :query page: page result
    :query count: count result per page
    """
    page = request.args.get("page", "1")
    count = request.args.get("count", "12")

    # type conversion
    page = int(page)
    count = int(count)

    teams_favorite = teamfavorite_ctrl.get_favorite(auth.user, page=page, count=count)

    result = []
    for fav in teams_favorite.items:
        result.append({
            "id": fav.team.id,
            "name": fav.team.name,
            "username": fav.team.
        })

    response = {
        "status": 200,
        "has_next": teams_favorite.has_next,
        "has_prev": teams_favorite.has_prev,
        "total": teams_favorite.total,
        "result": result
    }

    return jsonify(response)