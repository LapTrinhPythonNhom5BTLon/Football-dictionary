from flask import Blueprint, request, jsonify
from .services import get_player_data

player_name = Blueprint("player_name", __name__)

@player_name.route("/get-players/player", methods=["GET"])
def get_players():
    cau_thu = request.args.get("name")
    
    data = get_player_data(cau_thu)
    
    if not cau_thu:
        return jsonify({
            "message": "vui long nhap ten cau thu"
        }), 400 # loi cu phap
    
    elif len(data) == 0:
        return jsonify({
            "message": "khong tim thay cau thu nay"
        }), 404 # db khong co cau thu nay
    
    return jsonify({
        "message": "ok",
        "cau thu": data
    }), 200 # da tim thay