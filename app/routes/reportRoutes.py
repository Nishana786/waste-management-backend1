from flask import Blueprint

from flask_jwt_extended import jwt_required
from app.routehandler.reportRouteHandler import ReportRouteHandler

report_bp = Blueprint("report", __name__)


@report_bp.route("/report", methods=["POST"])
@jwt_required()
def create_report():
    return ReportRouteHandler.create_report()
