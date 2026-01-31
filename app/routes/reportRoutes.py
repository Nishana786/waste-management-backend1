from flask import Blueprint
from flask_cors import CORS
from flask_jwt_extended import jwt_required
from app.routehandler.reportRouteHandler import ReportRouteHandler

report_bp = Blueprint("report", __name__)

# 🔥 ENABLE CORS
CORS(report_bp)

@report_bp.route("/report", methods=["POST"])
@jwt_required()
def create_report():
    return ReportRouteHandler.create_report()
