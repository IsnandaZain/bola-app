from flask_sqlalchemy import Pagination
from soccer.exceptions import BadRequest, PlayerNotFound
from soccer.models import db, Player
from soccer.models import player as player_mdl


def create(shortname: str, fullname: str, backnumber: int, team_id: int, height: int = 0,
           weight: int = 0, nation: str = "Indonesia"):

    player = Player(shortname=shortname, fullname=fullname, back_number=backnumber)
    player.team_id = team_id
    player.nation = nation
    player.height = height
    player.weight = weight

    db.session.add(player)
    db.session.flush()

    return player


def update(player_id: int, shortname: str = None, fullname: str = None, backnumber: int = None, team_id: int = None,
           height: int = None, weight: int = None, nation: str = None):
    """Update event

    Args:
        player_id: id player yang di update
        shortname: nama punggung player yang di update
        fullname: nama lengkap player yang di update
        backnumber: nomor punggung baru player
        height: tinggi badan player
        weight: berat badan player
        nation: kebangsaan player
    
    Returns:
        Player object
    """
    player = player_mdl.get_by_id(player_id=player_id)

    # check apakah player exists
    if not player:
        raise PlayerNotFound

    if shortname is not None:
        player.shortname = shortname

    if fullname is not None:
        player.fullname = fullname

    if backnumber is not None:
        player.back_number = backnumber

    if team_id is not None:
        player.team_id = team_id

    if height is not None:
        player.height = height
    
    if weight is not None:
        player.weight = weight

    if nation is not None:
        player.nation = nation

    db.session.add(player)
    db.session.flush()

    return player


def get_list(page: int = 1, count: int = 1, team_id: str = None):
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

    if team_id:
        filters.append(Player.team_id == team_id)

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


def delete(player_id: int) -> Player:
    """Delete player by id
    Args:
        player_id: id player

    Returns:
    """
    player = player_mdl.get_by_id(player_id)
    if not player:
        raise PlayerNotFound

    player.is_deleted = 1
    db.session.add(player)
    db.session.flush()