from flask import Blueprint, request, jsonify, send_file

from soccer.controllers import player as player_ctrl
from soccer.exceptions import BadRequest, NotFound
from soccer.libs.ratelimit import ratelimit
from configuration import SoccerConfig


bp = Blueprint(__name__, "files")

@bp.route("/files/<path:path_file>")
def get_files(path_file):
    directory = path_file.split("/")[0]
    filename = path_file.split("/")[1]

    path_file_send = SoccerConfig.STORAGE_PATH + "/{}/{}".format(directory, filename)

    response = {
        "status": 200,
        "message": path_file_send
    }

    #return send_file(path_file_send, attachment_filename=filename)

    return jsonify(response), 400