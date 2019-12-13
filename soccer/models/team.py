import time
from datetime import datetime

from sqlalchemy.orm import relationship, backref

from soccer.models import db

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    shortname = db.Column(db.String, nullable=False)

    fullname = db.Column(db.String, nullable=False)

    liga = db.Column(db.Integer, nullable=False)

    stadion = db.Column(db.String, nullable=False)

    website = db.Column(db.String, default="")

    birthday = db.Column(db.String, default=None)

    created_on = db.Column(db.Integer, default=0)

    is_deleted = db.Column(db.Boolean, default=0)

    image = db.Column(db.String(100))

    image_icon = db.Column(db.String(100))

    image_thumb = db.Column(db.String(100))

    def __init__(self, shortname, fullname, liga, birthday):
        """
        Args:
            shortname: shortname dari team
            fullname: fullname dari team
            liga: liga yang diikuti team
        """
        self.shortname = shortname
        self.fullname = fullname
        self.liga = liga
        self.birthday = birthday

        self.created_on = time.time()


    def set_image(self, imagefile: str = None, filename: str = None):
        self.image = file.save(imagefile, 'teams', filename)

    @property
    def image_url(self):
        return file.url(self.image, 'teams')

    def set_image_icon(self, imagefile: str = None, filename: str = None):
        self.image_icon = file.save(imagefile, 'teams_icon', filename)

    @property
    def image_icon_url(self):
        return file.url(self.image_icon, 'teams_icon')

    def set_image_thumb(self, imagefile: str = None, filename: str = None):
        self.image_thumb = file.save(imagefile, 'teams_thumb', filename)

    @property
    def image_thumb_url(self):
        return file.url(self.image_thumb, 'teams_thumb')

    @property
    def avatar_json(self):
        return {
            "large": self.image,
            "medium": self.image_icon,
            "small": self.image_thumb
        }


def get_by_id(team_id: int) -> Team:
    return Team.query.filter_by(id=team_id).first()
