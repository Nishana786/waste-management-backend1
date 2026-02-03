from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.routehandler.dashboardRouteHandler import DashboardRouteHandler

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard/stats", methods=["GET"])
@jwt_required()
def dashboard_stats():
    try:
        user_id = get_jwt_identity()

        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401

        # Handler call (user_id pass cheyyanam)
        data = DashboardRouteHandler.get_stats(user_id)

        return jsonify(data), 200

    except Exception as e:
        print("Dashboard stats error:", e)
        return jsonify({"error": "Internal Server Error"}), 500
