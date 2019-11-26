__author__ = "isnanda.muhammadzain@sebangsa.com"


class SoccerException(Exception):
    """Indicates that the request could not be processed because of request in client is invalid"""
    
    message = __doc__.strip()
    status_code = 400
    payload = None

    def __init__(self, message=None, status_code, payload=None):

        if message is not None:
            self.message = message

        if status_code is not None:
            self.status_code = status_code

        if payload is not None:
            self.payload = payload

        super(SoccerException, self).__init__(self.message)

    def to_dict(self):
        res = {
            "message": self.message
        }

        if self.payload:
            for key, value in self.payload.items():
                res[key] = value
        
        return res


class BadRequest(SoccerException):
    """Indicates that the query was invalid.
    E.g. some parameter missing."""

    message = __doc__.strip()
    status_code = 400


class TeamNotFound(BadRequest):
    message = "Team tidak ditemukan"


class PlayerNotFound(BadRequest):
    message = "Player tidak ditemukan"


class NotFound(SoccerException):
    """Indicates that the request data is not exists.
    E.g. data missing, endpoint not found"""

    message = __doc__.strip()
    status_coded = 404