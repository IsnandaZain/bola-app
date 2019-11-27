from flask import Blueprint, request, jsonify

from soccer.controllers import teamfavorite as teamfavorite_ctrl
from soccer.exceptions import BadRequest
from soccer.libs.ratelimit import ratelimit


bp = Blueprint(__name__, "team_favorite")


@bp.route("/team/favorite", methods=["POST"])
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
                {
                    "favorite_id": 1,
                    "team": {
                        "id": 1,
                        "shortname": FCB,
                        "fullname": Barcelona FC,
                        "liga": {
                            "id": 1,
                            "name": La Liga,
                            "nation": Spain,
                            "image": asset.soccer-app...,
                            "image_icon": asset.soccer-app...,
                            "image_thumb": asset.soccer-app...,
                        },
                        "website": www.barcelona.com,
                        "birthday": 1556789851,
                        "image": asset.soccer-app...,
                        "image_icon": asset.soccer-app...,
                        "image_thumb": asset.soccer-app...,
                    }
                }
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
            "favorite_id": fav.team.id,
            "team": {
                "id": fav.team.id,
                "shortname": fav.team.shortname,
                "fullname": fav.team.fullname,
                "liga": {
                    "id": fav.team.liga.id,
                    "name": fav.team.liga.name,
                    "nation": fav.team.liga.nation,
                    "image": fav.team.liga.image_url,
                    "image_icon": fav.team.liga.image_icon_url,
                    "image_thumb": fav.team.liga.image_thumb_url,
                },
                "website": fav.team.website,
                "birthday": fav.team.birthday,
                "image": fav.team.image_url,
                "image_icon": fav.team.image_icon_url,
                "image_thumb": fav.team.image_thumb_url,
            }
        })

    response = {
        "status": 200,
        "has_next": teams_favorite.has_next,
        "has_prev": teams_favorite.has_prev,
        "total": teams_favorite.total,
        "result": result
    }

    return jsonify(response)