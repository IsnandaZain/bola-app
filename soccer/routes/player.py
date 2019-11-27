from flask import Blueprint, request, jsonify

from soccer.controllers import player as player_ctrl
from soccer.exceptions import BadRequest, NotFound
from soccer.libs.ratelimit import ratelimit


bp = Blueprint(__name__, "player")

@bp.route("/player", methods=["GET"])
def player_list():
    """Get list player

    **endpoint**

    .. sourcecode:: http

        GET /player

    **success response**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: text/javascript

        {
            "status": 200,
            "has_next": false,
            "has_prev": false,
            "total": 1,
            "result": [
                {
                    "id": 1,
                    "shortname": Messi,
                    "fullname": Lionel Messi,
                    "backnumber": 10,
                    "height": 165,
                    "weight": 61,
                    "nation": Argentina,
                    "team": {
                        "id": 1,
                        "shortname": FCB,
                        "fullname": Bacelona FC,
                        "liga": La Liga,
                        "stadion": Camp Nou,
                        "image": asset.soccer-app...,
                        "image_icon": asset.soccer-app...,
                        "image_thumb": asset.soccer-app...,
                    },
                    "image": asset.soccer-app...,
                    "image_icon": asset.soccer-app...,
                    "image_thumb": asset.soccer-app...,
                }
            ]
        }

    :query page: pagination page
    :query count: count result per page
    :query team: team yang akan dicari list pemainnya
    """
    page = request.args.get("page", "1")
    count = request.args.get("count", "12")
    team = request.args.get("team")

    # type conversion
    page = int(page)
    count = int(count)

    if not team:
        raise BadRequest("Nama team tidak boleh kosong")

    player = player_ctrl.get_list(page=page, count=count, team=team)

    response = {
        "status": 200 if player.items != [] else 204,
        "has_next": player.has_next,
        "has_prev": play.has_prev,
        "total": player.total,
        "result": _entity_player_list(player.items)
    }

    return jsonify(response)


def _entity_player_list(players):
    results = []
    for player in players:
        results.append({
            "id": player.id,
            "shortname": player.shortname,
            "fullname": player.fullname,
            "backnumber": player.backnumber,
            "height": player.height,
            "weight": player.weight,
            "nation": player.nation,
            "team": {
                "id": player.team.id,
                "shortname": player.team.shortname,
                "fullname": player.team.fullname,
                "liga": player.team.liga,
                "stadion": player.team.stadion,
                "image": player.team.image_url,
                "image_icon": player.team.image_icon_url,
                "image_thumb": player.team.image_thumb_url,
            },
            "image": player.image_url,
            "image_icon": player.image_icon_url,
            "image_thumb": player.image_thumb_url,
        })


    return results


@bp.route("/player/<int:player_id>", methods=["GET"])
def player_get_by_id(player_id):
    """Get player by id

    **endpoint**

    .. sourcecode:: http

        GET /player/<int:player_id>

    **success response**

        HTTP/1.1 200 OK
        Content-Type: text/javascript

        {
            "status": 200,
            "id": 1,
            "shortname": Messi,
            "fullname": Lionel Messi,
            "backnumber": 10,
            "height": 165,
            "weight": 61,
            "nation": Argentina,
            "team": {
                "id": 1,
                "shortname": FCB,
                "fullname": Barcelona FC,
                "liga": La Liga,
                "stadion": Camp Nou,
                "image": asset.soccer-app...,
                "image_icon": asset.soccer-app...,
                "image_thumb": asset.soccer-app...,
            },
            "image": asset.soccer-app...,
            "image_icon": asset.soccer-app...,
            "image_thumb": asset.soccer-app...,
        }
    """
    player = player_ctrl.get(player_id=player_id)

    response = {
        "status": 200,
        "id": player.id,
        "shortname": player.shortname,
        "fullname": player.fullname,
        "backnumber": player.backnumber,
        "height": player.height,
        "weight": player.weight,
        "nation": player.nation,
        "team": {
            "id": player.team.id,
            "shortname": player.team.shortname,
            "fullname": player.team.fullname,
            "liga": player.team.liga,
            "stadion": player.team.stadion,
            "image": player.team.image_url,
            "image_icon": player.team.image_icon_url,
            "image_thumb": player.team.image_thumb_url,
        },
        "image": player.image_url,
        "image_icon": player.image_icon_url,
        "image_thumb": player.image_thumb_url,
    }

    return jsonify(response)