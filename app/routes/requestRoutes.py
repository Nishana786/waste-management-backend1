from flask import Blueprint
from flask_cors import CORS
from flask_jwt_extended import jwt_required
from app.routehandler.requestRouteHandler import RequestRouteHandler

request_bp = Blueprint("request", __name__)

# 🔥 ENABLE CORS
CORS(request_bp)

@request_bp.route("/request", methods=["POST"])
@jwt_required()
def create_request():
    return RequestRouteHandler.create_request()
