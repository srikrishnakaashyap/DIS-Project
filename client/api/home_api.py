from flask import Blueprint, request, redirect, url_for, render_template
from constants.global_constants import GC

from services.command_service import CommandService as CS
import json

home_blueprint = Blueprint("home", __name__, template_folder="templates")


@home_blueprint.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        GC.USERNAME = request.form["username"]
        GC.PASSWORD = request.form["password"]
        GC.CLIENT_DIR = f"{GC.USERNAME}_dir"
        # print(session["USERNAME"], session["PASSWORD"])
        client_socket = CS.makeConnection(GC.USERNAME, GC.PASSWORD, GC.CLIENT_DIR)

        print("CLIENT SOCKET", client_socket)
        print(GC.CLIENT_SOCKET)

        if not client_socket:
            return render_template(
                "login.html",
                message="Invalid Authentication or Server is unavailable",
            )

        # session["CLIENT_SOCKET"] = client_socket

        return redirect("/command")
    return render_template("login.html")
