from flask_sqlalchemy import Pagination

from string import punctuation

from soccer.models import db, Team


def search_team(keyword: str, page: int = 1, count: int = 12) -> Pagination:
    """Search teams

    Args:
        keyword: keyword for search
        page: number of page
        count: item per page
    
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