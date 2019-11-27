from flask import Blueprint, request, jsonify

from datetime import datetime

from soccer.controllers import standing as standing_ctrl
from soccer.exceptions import BadRequest, NotFound


bp = Blueprint(__name__, "standing")


@bp.route("/standing", methods=["GET"])
def standing_list():
    """Get list team in standing

    **endpoint**

    .. sourcecode:: http

        GET /standing

    **success response**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: text/javascript

        {
            "status": 200,
            "result": [
                {

                }
            ]
        }

    :query liga: liga yang akan ditampilkan standing listnya
    """
    liga = request.args.get("liga")
    periode = request.args.get("periode")

    if not liga:
        raise BadRequest("Nama liga tidak boleh kosong")

    if not liga:
        periode = datetime.today().year

    standing = standing_ctrl.get(liga=liga, periode=periode)

    response = {
        "status": 200 if standing != [] else 204,
        "result": _entity_standing_list(standing)
    }

    return jsonify(response)


def _entity_standing_list(standings):
    results = []
    for standing in standings:
        results.append({
            "position": standing.position,
            "points": standing.points,
            "periode": standing.periode,
            "team": {
                "id": standing.team.id,
                "shortname": standing.team.shortname,
                "fullname": standing.team.fullname,
                "website": standing.team.website,
                "birthday": standing.team.birthday,
                "image": standing.team.image_url,
                "image_icon": standing.team.image_icon_url,
                "image_thumb": standing.team.image_thumb_url,
            }
        })

    return results