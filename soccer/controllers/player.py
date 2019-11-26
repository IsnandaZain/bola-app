from flask_sqlalchemy import Pagination
from soccer.exceptions import BadRequest, PlayerNotFound
from soccer.models import db, Players
from soccer.models import player as player_mdl


def get_list(page: int = 1, count: int = 1, team: str = None):
    """Get player with pagination

    Args:
        page: page start
        count: count per page
        team: team yang dipilih

    Returns:
        Pagination
    """
    filters = [
        Players.is_deleted == 0
    ]

    if team:
        filters.append(Players.team == team)

    players = Players.query.filter(
        *filters
    ).order_by(
        Players.id.desc()
    ).paginate(
        page=page,
        per_page=count,
        error_out=False,
    )

    return players


def get(player_id: int) -> Players:
    """Get player by id
    Args:
        player_id: id player

    Returns:
        Player
    """
    player = plyer_mdl.get_by_id(player_id)
    if not player:
        raise PlayerNotFound

    return player