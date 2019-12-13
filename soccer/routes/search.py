from flask import Blueprint, request, jsonify

from soccer.controllers import search
from soccer.exceptions import BadRequest
from soccer.libs.ratelimit import ratelimit

from soccer.models import team as team_mdl
from soccer.models import player as player_mdl

bp = Blueprint(__name__, 'search')


@bp.route("/search/team")
def search_team():
    """Search team

    **endpoint**

    .. sourcecode:: http

        GET /search/team

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
                    },
                    "website": www.barcelona.com,
                    "birthday": 1555769584,
                    "image": asset.soccer-app...,
                    "image_icon": asset.soccer-app...,
                    "image_thumb": asset.soccer-app...,
                }
            ]
        }

    :query keyword: keyword for search
    :query next_id: start id team for search
    :query last_id: last_id team fro search
    :query page: pagination page
    :query count: count result per page

    optional:
    :query sort: sort list team
        - match: sort by match query
        - id: sort id by id asc
        - -id: sort id by id desc
        - name: sort by name asc
        - -name: sort by name desc
    """
    keyword = request.args.get("keyword")
    page = request.args.get("page", "1")
    count = request.args.get("count", "12")
    sort = request.args.get("sort", "match")
    next_id = request.args.get("next_id", "0")
    last_id = request.args.get("last_id", "0")

    # raise BadRequest is missing keyword
    if not keyword:
        raise BadRequest("Keyword kosong")

    if not page.isdigit() or not count.isdigit():
        raise BadRequest("page dan count harus integer")

    if sort and sort not in ("-id", "id", "match", "-name", "name"):
        raise BadRequest("Sort tidak didukung")

    # type conversion
    page = int(page)
    count = int(count)
    next_id = int(next_id)
    last_id = int(last_id)
    
    teams = search.search_team(keyword, next_id, last_id, page, count, sort)

    # get teams result
    result = []
    if teams != None:
        for team in teams.items:
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


    response = {
        "status": 200,
        "result": result,
        "has_prev": teams.has_prev if teams else False,
        "has_next": teams.has_next if teams else False,
        "total": teams.total if teams else 0
    }

    return jsonify(response)


@bp.route("/search/player")
def search_player():
    """Search player

    **endpoint**

    .. sourcecode:: http

        GET /search/player

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

                }
            ]
        }

    :query keyword: keyword for search
    :query next_id: start id player for search
    :query last_id: last id player for search
    :query page: pagination pag
    :query count: count result per page

    optional:
    :query sort: sort list player
        - match: sort by match query
        - id: sort by id asc
        - -id: sort by id desc
        - name: sort by name asc
        - -name: sort by name desc
    """
    keyword = request.args.get("keyword")
    page = request.args.get("page", "1")
    count = request.args.get("count", "12")
    sort = request.args.get("sort", "match")
    next_id = request.args.get("next_id")
    last_id = request.args.get("last_id")

    # raise BadRequest is missing keyword
    if not keyword:
        raise BadRequest("Keyword kosong")

    if not page.isdigit() or not count.isdigit():
        raise BadRequest("page dan count harus integer")

    if sort and sort not in ("-id", "id", "match", "name", "-name"):
        raise BadRequest("Sort tidak didukung")

    # type conversion
    page = int(page)
    count = int(count)
    next_id = int(next_id)
    last_id = int(last_id)

    players = search.search_player(keyword, next_id, last_id, page, count, sort)

    # get players result
    result = []
    if players != None:
        for player in players.items:


    response = {
        "status": 200,
        "result": result,
        "has_prev": players.has_prev if players else False,
        "has_next": players.has_next if players else False,
        "total": players.total if players else 0
    }

    return jsonify(response)