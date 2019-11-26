from flask_sqlalchemy import Pagination

from soccer.exceptions import BadRequest
from soccer.models import db, TeamFavorites


def set_favorite(actor: int, team_id: int) -> UserFavorites:
    """Action favorite user

    Args:
        actor: actor yang akan melakukan favorite
        team_id: id team yang akan difavoritkan
    """
    # check sudah difavoritkan apa belum
    team = UserFavorites.query.filter_by().first()
    if team:
        raise BadRequest("Team sudah masuk kedalam daftar favorite")

    # set favorite
    favorite = TeamFavorites(actor, team_id)
    db.session.add(favorite)

    db.session.flush()
    return favorite


def set_unfavorite(actor: int, team_id: int) -> None:
    """Action unfavorite user

    Args:
        actor: actor yang akan melakukan unfavorite
        team_id: id team yang akan di unfavoritkan
    """
    # check apakah sudah di favoritkan atau belum
    favorite = TeamFavorites.query.filter_by().first()
    if not favorite:
        raise BadRequest("Team tidak pernah di favorite")

    # set unfavorite
    favorite.is_deleted = 1
    db.session.add(favorite)


def get_favorite(user: Users, page: int = 1, count: int = 20) -> Pagination:
    """Get list of favorite team

    Args:
        user: user yang akan diambil list favoritenya
        page: number of page
        count: item per page

    Returns:
        list team yang difavoritkan
    """
    user_favorite = UserFavorites.query.filter_by().paginate(
        page=page,
        per_page=count,
        error_out=False
    )

    return user_favorite