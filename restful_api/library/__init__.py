from flask import Flask
from .players.controller import player_name as pn
from .team.controller import team_name as tn

def create_app(config_file = "config.py"):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    app.json.sort_keys = False
    
    app.register_blueprint(pn)
    app.register_blueprint(tn)
    
    return app