from flask_sqlalchemy import Pagination
from soccer.exceptions import BadRequest
#from soccer.models import db, Standing
#from soccer.models import standing as standing_mdl


def get(liga: str, periode: int) -> Pagination:
    """Get standing from liga

    Args:
        liga: liga yang akan ditampilkan standingnya
        periode: periode liga yang ditampilkan

    Returns:
        Pagination
    """
    print("nilai periode : ", periode)