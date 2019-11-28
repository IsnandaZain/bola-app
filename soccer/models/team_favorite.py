import time

from sqlalchemy.orm import relationship, backref

from soccer.models import db


class TeamFavorites(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    team_id = db.Column(db.Integer, db.ForeignKey("team.id"))

    is_deleted = db.Column(db.Boolean, default=0)

    created_on = db.Column(db.Integer, default=0)

    """
    user = relationship("Users", backref=backref("team_favorites", lazy="dynamic"),
                        primaryjoin="and_(TeamFavorites.user_id==Users.id, "
                                    "TeamFavorites.is_deleted==0)")

    team = relationship("Team", backref=backref("team_favorites", lazy="dynamic"))
    """
    
    def __init__(self, user_id, team_id):
        self.user_id = user_id,
        self.team_id = team_id
        
        self.created_on = time.time()