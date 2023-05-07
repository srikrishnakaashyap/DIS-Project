from flask import Blueprint, request, redirect, url_for, render_template
from constants.global_constants import GC

from services.command_service import CommandService as CS
import json

command_blueprint = Blueprint("command", __name__, template_folder="templates")


@command_blueprint.route("/command", methods=["GET", "POST"])
def command():
    if request.method == "POST":
        command = request.form["command"]

        client_socket = GC.CLIENT_SOCKET
        # print("SOCKET", client_socket)
        if not client_socket:
            return render_template(
                "login.html", message="Client Disconnected. Please Login Again"
            )
        print("QUERY", command)
        result = CS.sendCommand(command, GC.CLIENT_DIR)
        print("RESULT", result)

        GC.COMMAND_HISTORY.append({command: result})
        return render_template("command.html", command_history=GC.COMMAND_HISTORY)
    else:
        return render_template("command.html", command_history=GC.COMMAND_HISTORY)
