from flask_sqlalchemy import Pagination
from soccer.exceptions import BadRequest, TeamNotFound
from soccer.models import db, Team
from soccer.models import team as team_mdl


def get_list(page: int = 1, count:int = 12, liga: str = None) -> Pagination:
    """Get teams with pagination

    Args:
        page: page start
        count: count per page
        liga: liga yang dipilih

    Returns:
        Pagination
    """
    filters = [
        Team.is_deleted == 0,
    ]

    if liga:
        filters.append(Team.liga == liga)

    teams = Team.query.filter(
        *filters
    ).order_by(
        Team.id.desc()
    ).paginate(
        page=page,
        per_page=count,
        error_out=False,
    )

    return teams


def get(team_id: int) -> Team:
    """Get team by id
    Args:
        team_id: id team

    Returns:
        Team
    """
    team = team_mdl.get_by_id(team_id)
    if not team:
        raise TeamNotFound

    return team