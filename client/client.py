import time
from flask import Flask, request, session, render_template
import socket
import os
import time
from werkzeug.middleware.proxy_fix import ProxyFix
from initializers.register_blueprints import RegisterBlueprints

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_port=1)


with app.app_context():
    RegisterBlueprints(app)
    app.run(
        host="0.0.0.0",
        port=5001,
    )
