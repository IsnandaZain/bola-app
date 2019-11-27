import time

from sqlalchemy.orm import relationship, backref

from soccer.models import db

class Standings(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    team_id = db.Column(db.Integer, db.ForeignKey("team.id"))

    liga_id = db.Column(db.Integer, db.ForeignKey("league.id"))

    position = db.Column(db.Integer, default=0)

    periode = db.Column(db.Integer, nullable=False)

    points = db.Column(db.Integer, default=0)

    def __init__(self, team_id, liga_id):
        """
        Args:
            team_id: id team yang masuk standing
            liga_id: liga id dari standing
        """
        self.team_id = team_id
        self.liga_id = liga_id
    
    
