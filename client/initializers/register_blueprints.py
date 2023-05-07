from api.command_api import command_blueprint
from api.home_api import home_blueprint


class RegisterBlueprints:
    def __init__(self, app):
        app.register_blueprint(command_blueprint)
        app.register_blueprint(home_blueprint)
