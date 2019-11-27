from flask_sqlalchemy import Pagination
from soccer.exceptions import BadRequest, PlayerNotFound
from soccer.models import db, Player
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
        Player.is_deleted == 0
    ]

    if team:
        filters.append(Player.team == team)

    players = Player.query.filter(
        *filters
    ).order_by(
        Player.id.desc()
    ).paginate(
        page=page,
        per_page=count,
        error_out=False,
    )

    return players


def get(player_id: int) -> Player:
    """Get player by id
    Args:
        player_id: id player

    Returns:
        Player
    """
    player = player_mdl.get_by_id(player_id)
    if not player:
        raise PlayerNotFound

    return player