from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.routehandler.dashboardRouteHandler import DashboardRouteHandler

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard/stats", methods=["GET", "OPTIONS"])
@jwt_required(optional=True)
def dashboard_stats():

    # ✅ Preflight request handle
    if request.method == "OPTIONS":
        return "", 200

    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = DashboardRouteHandler.get_stats(user_id)
    return jsonify(data), 200
