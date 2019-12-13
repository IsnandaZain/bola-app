from flask_sqlalchemy import Pagination

from string import punctuation

from soccer.models import db, Team, Player


def search_team(keyword: str, page: int = 1, count: int = 12, next_id: int = 0, last_id: int = 0) -> Pagination:
    """Search teams

    Args:
        keyword: keyword for search
        page: number of page
        count: item per page
        next_id: next id team yang dicari
        last_id: last id team yang dicari
    
    Returns:
        Pagination
    """
    keyword = keyword.strip(punctuation)
    if keyword == "":
        return None

    filter_apply = [Teams.fullname.like("%{}%".format(keyword))]

    if next_id:
        filter_apply.append(Teams.id < next_id)

    if last_id:
        filter_apply.append(Teams.id > last_id)

    # generate query sort
    sort_collections = {
        "-name": Teams.name.desc(),
        "name": Teams.name.asc(),
        "-id": Teams.id.desc(),
        "id": Teams.id.asc(),
        "match": db.case(
            (
                (Teams.name == keyword, 0),
                (Teams.name.like("{}%".format(keyword)), 1),
                (Teams.name.like("%{}%".format(keyword)), 2),
                (Teams.name.like("%{}".format(keyword)), 3)
            ), else_=4
        ).asc()
    }

    sort_apply = sort_collections[sort]

    teams = Teams.query.filter(
        *filter_apply
    ).order_by(
        sort_apply
    ).paginate(
        page=page,
        per_page=count,
        error_out=False
    )

    return teams


def search_player(keyword: str, page: int = 1, count: int = 12, next_id: int = 0, last_id: int = 0) -> Pagination:
    """Search players

    Args:
        keyword: keyword players
        page: number of page
        count: item per page
        next_id: next id player yang dicari
        last_id: last id player yang dicari

    Returns:
        Pagination
    """
    keyword = keyword.strip(punctuation)
    if keyword == "":
        return None

    filter_apply = [Player.fullname.like("%{}%".format(keyword))]

    if bool(next_id):
        filter_apply.append(Player.id < next_id)

    if bool(last_id):
        filter_apply.append(Player.id > last_id)

    # generate query sort
    sort_collections = {
        "-name": Player.name.desc(),
        "name": Player.name.asc(),
        "-id": Player.id.desc(),
        "id": Player.id.asc(),
        "match": db.case(
            (
                (Player.name == keyword, 0),
                (Player.name.like("{}%".format(keyword)), 1)
                (Player.name.like("%{}%".format(keyword)), 2)
                (Player.name.like("%{}".format(keyword)), 3)
            ), else_=4
        ).asc()
    }

    sort_apply = sort_collections[sort]

    players = Player.query.filter(
        *filter_apply
    ).order_by(
        sort_apply
    ).paginate(
        page=page,
        per_page=count,
        error_out=False
    )

    return players