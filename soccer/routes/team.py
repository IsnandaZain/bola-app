from flask import Blueprint, request, jsonify

from soccer.controllers import team as team_ctrl
from soccer.exceptions import BadRequest, NotFound


bp = Blueprint(__name__, "team")

@bp.route("/team/create", methods=["POST"])
def team_create():
    """Create team

    **endpoint**

    .. sourcecode:: http

        POST /team/create

    **success response**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: text/javascript

        {
            status: 200,
            id: 1,
            shortname: FCB,
            fullname: FC Barcelona,
            liga: La Liga Spanyol,
            stadion: Camp Nou,
            website: www.fcbarcelona.com,
            birthday: DD-MM-YYYY
        }

    :form shortname: nama pendek dari team
    :form fullname: nama lengkap dari team
    :form liga: nama liga yang diikuti team
    :form stadion: nama stadion kandang team
    :form website: website official dari team
    :form birthday: tanggal club lahir
    """
    shortname = request.form.get("shortname")
    fullname = request.form.get("fullname")
    liga = request.form.get("liga")
    stadion = request.form.get("stadion")
    website = request.form.get("website")
    birthday = request.form.get("birthday")

    if None in (shortname, fullname):
        raise BadRequest("shortname, fullname tidak boleh kosong")

    if not birthday.isdigit():
        raise BadRequest("birthday harus integer")

    # type conversion
    birthday = int(birthday)
    
    team = team_ctrl.create(
        shortname=shortname,
        fullname=fullname,
        liga=liga,
        stadion=stadion,
        website=website,
        birthday=birthday
    )

    response = {
        "status": 200,
        "id": team.id,
        "shortname": team.shortname,
        "fullname": team.fullname,
        "liga": team.liga,
        "stadion": team.stadion,
        "website": team.website,
        "birthday": team.birthday,
        "avatar": team.avatar_json,
    }

    return jsonify(response)
    

@bp.route("/team", methods=["GET"])
def team_list():
    """Get list team

    **endpoint**

    .. sourcecode:: http

        GET /team

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
                    "birhtday": 1555867523,
                    "image": asset.soccer-app...,
                    "image_icon": asset.soccer-app...,
                    "image_thumb": asset.soccer-app...,
                }
            ]
        }

    :query page: pagination pag
    :query count: count result per page
    :query league: liga yang dipilih
    """
    page = request.args.get("page", "1")
    count = request.args.get("count", "12")
    liga = request.args.get("league")

    if not liga:
        raise BadRequest("Nama liga tidak boleh kosong")

    # type conversion
    page = int(page)
    count = int(count)

    team = team_ctrl.get_list(page=page, count=count, liga=liga)

    response = {
        "status": 200 if team.items != [] else 204,
        "has_next": team.has_next,
        "has_prev": team.has_prev,
        "total": team.total,
        "result": _entity_team_list(team.items)
    }

    return jsonify(response)


def _entity_team_list(teams):
    results = []
    for team in teams:
        result.append({
            "id": team.id,
            "shortname": team.shortname,
            "fullname": team.fullname,
            "liga": {
                "id": team.liga.id,
                "name": team.liga.name,
                "nation": team.liga.nation,
                "image": team.liga.image_url,
                "image_icon": team.liga.image_icon_url,
                "image_thumb": team.liga.image_thumb_url,
            },
            "website": team.website,
            "birthday": team.birthday,
            "image": team.image_url,
            "image_icon": team.image_icon_url,
            "image_thumb": team.image_thumb_url,
        })

    return results


@bp.route("/team/<int:team_id>", methods=["GET"])
def team_get_by_id(team_id):
    """Get team by id

    **endpoint**

    .. sourcecode:: http

        GET /team/<int:team_id>

    **success response**

        HTTP/1.1 200 OK
        Content-Type: text/javascript

        {
            "status": 200,
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
            }
        }
    """
    team = team_ctrl.get(team_id=team_id)

    response = {
        "status": 200,
        "id": team.id,
        "shortname": team.shortname,
        "fullname": team.fullname,
        "liga": {
            "id": team.liga.id,
            "name": team.liga.name,
            "nation": team.liga.nation,
            "image": team.liga.image_url,
            "image_icon": team.liga.image_icon_url,
            "image_thumb": team.liga.image_thumb_url,
        },
        "website": team.website,
        "birthday": team.birthday,
        "image": team.image_url,
        "image_icon": team.image_icon_url,
        "image_thumb": team.image_thumb_url,
    }

    return jsonify(response)


@bp.route("/team/update", methods=["UPDATE"])
def team_update():
    """Update team

    **endpoint**

    .. sourcecode:: http

        UPDATE /team/update

    **success response**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: text/javascript

        {
            "status": 200,
            "id": 1,
            "message": "Berhasil mengupdate informasi team"
        }

    """
    team_id = request.form.get("team_id")
    

    if not team_id:
        raise BadRequest("team id tidak boleh kosong")

    # type conversion
    team_id = int(team_id)


    team = team_ctrl.update(

    )

    response = {
        "id": team.id,
        "status": 200,
        "message": "Berhasil mengupdate informasi team"
    }

    return jsonify(response)


@bp.route("/team/delete/<int:team_id>", methods=["DELETE"])
def team_delete():
    """Delete team

    **endpoint**

    .. sourcecode:: http

        POST /team/delete/<int:team_id>

    **success response**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: text/javascript

        {
            "status": 200,
            "message": "Berhasil menghapus player"
        }
    """
    # type conversion
    team_id = int(team_id)

    team_ctrl.delete(team_id=team_id)

    response = {
        "status": 200,
        "message": "Berhasil menghapus team"
    }

    return jsonify(response)