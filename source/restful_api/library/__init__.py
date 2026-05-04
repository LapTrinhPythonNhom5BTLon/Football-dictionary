from flask import Flask
from .players.controller import player_name as pn
from .team.controller import team_name as tn

def create_app():
    app = Flask(__name__)
    app.json.sort_keys = False
    
    app.register_blueprint(pn)
    app.register_blueprint(tn)
    
    return app