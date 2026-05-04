from flask import Blueprint, request, jsonify
from .services import get_team_data

team_name = Blueprint("team_name", __name__)
@team_name.route("/get-teams/team", methods=["GET"])
def get_teams():
    doi_bong = request.args.get("name")
    
    data = get_team_data(doi_bong)
    
    if not doi_bong:
        return jsonify({
            "message": "vui long nhap ten doi bong"
        }), 400
    
    elif len(data) == 0:
        return jsonify({
            "message": "khong tim thay doi bong nay"
        }), 404
    
    return jsonify({
        "message": "ok",
        "doi bong": data
    })