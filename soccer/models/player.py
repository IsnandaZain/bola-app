import time

from sqlalchemy.orm import relationship, backref

from soccer.models import db


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    shortname = db.Column(db.String, nullable=False)

    fullname = db.Column(db.String, nullable=False)

    backnumber = db.Column(db.Integer, nullable=False)

    height = db.Column(db.Integer, nullable=False)

    weight = db.Column(db.Integer, nullable=False)

    nation = db.Column(db.String, nullable=False)

    created_on = db.Column(db.Integer, default=0)

    team_id = db.Column(db.Integer, db.ForeignKey("team.id"))

    image = db.Column(db.String(100))

    image_icon = db.Column(db.String(100))

    image_thumb = db.Column(db.String(100))

    team = relationship("")

    def __init__(self, shortname, fullname, back_number):
        """
        Args:
            shortname: shortname dari pemain
            fullname: fullname dari pemain
            back_number: nomor punggung dari pemain
        """
        self.shortname = shortname
        self.fullname = fullname
        self.back_number = back_number

        self.created_on = time.time()


    def set_image(self, imagefile: str = None, filename: str = None):
        self.image = file.save(imagefile, 'players', filename)

    @property
    def image_url(self):
        return file.url(self.image, 'players')

    def set_image_icon(self, imagefile: str = None, filename: str = None):
        self.image_icon = file.save(imagefile, 'players_icon', filename)

    @property
    def image_icon_url(self):
        return file.url(self.image_icon, 'players_icon')

    def set_image_thumb(self, imagefile: str = None, filename: str = None):
        self.image_thumb = file.save(imagefile, 'players_thumb', filename)

    @property
    def image_thumb_url(self):
        return file.url(self.image_thumb, 'players_thumb')
