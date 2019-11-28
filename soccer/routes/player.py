from flask import Blueprint, request, jsonify

from soccer.controllers import player as player_ctrl
from soccer.exceptions import BadRequest, NotFound
from soccer.libs.ratelimit import ratelimit


bp = Blueprint(__name__, "player")

@bp.route("/player/create", methods=["POST"])
def player_create():
    """Create player

    **endpoint**

    .. sourcecode:: http

        POST /player/create

    **success response**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: text/javascript

        {
            "status": 200,
            "id": 1,
            "shortname": "Messi",
            "fullname": "Lionel Messi",
            "backnumber": 10,
            "height": 165,
            "weight": 60,
            "nation": Argentina,
            "team_id": 1,
            "avatar": {
                "large": "",
                "medium": "",
                "small": "",
            }
        }

    :form shortname: nama punggung dari pemain
    :form fullname: nama lengkap dari pemain
    :form backnumber: nomor punggung dari pemain
    :form height: tinggi dari pemain
    :form weight: berat badan pemain
    :form nation: kebangsaan dari pemain
    :form team_id: id team pemain
    """
    shortname = request.form.get("shortname")
    fullname = request.form.get("fullname")
    backnumber = request.form.get("backnumber")
    height = request.form.get("height", "0")
    weight = request.form.get("weight", "0")
    nation = request.form.get("nation", "Indonesia")
    team_id = request.form.get("team_id", "1")

    if None in (shortname, fullname, backnumber):
        raise BadRequest("shortname, fullname, backnumber tidak boleh kosong")

    # type conversion
    backnumber = int(backnumber)
    height = int(height)
    weight = int(weight)
    team_id = int(team_id)

    player = player_ctrl.create(
        shortname=shortname,
        fullname=fullname,
        backnumber=backnumber,
        team_id=team_id,
        height=height,
        weight=weight,
        nation=nation
    )

    response = {
        "status": 200,
        "id": player.id,
        "shortname": player.shortname,
        "fullname": player.fullname,
        "backnumber": player.back_number,
        "height": player.height,
        "weight": player.weight,
        "nation": player.nation,
        "team": player.team_id,
        "avatar": player.avatar_json,
    }

    return jsonify(response)


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
    team_id = request.args.get("team_id")

    # type conversion
    page = int(page)
    count = int(count)
    team_id = int(team_id)

    if not team_id:
        raise BadRequest("Nama team tidak boleh kosong")

    player = player_ctrl.get_list(page=page, count=count, team_id=team_id)

    response = {
        "status": 200 if player.items != [] else 204,
        "has_next": player.has_next,
        "has_prev": player.has_prev,
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
            "team_id": player.team_id,
            "avatar": player.avatar_json,
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
        "team_id": player.team_id,
        "avatar": player.avatar_json,
    }

    return jsonify(response)