from flask_sqlalchemy import Pagination
from soccer.exceptions import BadRequest, TeamNotFound
from soccer.models import db, Team
from soccer.models import team as team_mdl


def create(shortname: str, fullname: str, liga: str, stadion: str,
           website: str, birthday: int):
    """Create a new team

    Args:
        shortname: nama pendek dari club
        fullname: nama panjang dari club
        liga: nama liga yang diikuti club
        stadion: nama stadion kandang club
        website: website official club
        birthday: tanggal lahir club

    Returns:
        Team Object
    """
    team = Team(shortname=shortname, fullname=fullname, liga=liga)
    team.stadion = stadion
    team.website = website
    team.birthday = birthday

    db.session.add(team)
    db.session.flush()

    return team


def update(team_id: int, shortname: str = None, fullname: str = None, liga: str = None,
           stadion: str = None, website: str = None, birthday: int = None):
    """Update team

    Args:
        team_id: id club yang di update
        shortname: nama pendek dari club
        fullname: nama lengkap dari club
        liga: nama liga yang diikuti club
        stadion: nama stadion kandang club
        website: website official club
        birthday: tanggal lahir club

    Returns:
        Team object
    """
    team = team_mdl.get_by_id(team_id=team_id)

    # check apakah team exists
    if not team:
        raise TeamNotFound

    if shortname is not None:
        team.shortname = shortname

    if fullname is not None:
        team.fullname = fullname

    if stadion is not None:
        team.stadion = stadion

    if website is not None:
        team.website = website

    db.session.add(team)
    db.session.flush()

    return team


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