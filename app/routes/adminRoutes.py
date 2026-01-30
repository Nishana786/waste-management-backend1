from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.utils.admin_required import admin_required
from app.routehandler.adminRouteHandler import AdminRouteHandler

admin_bp = Blueprint("admin", __name__)

# ================= ADMIN DASHBOARD =================
@admin_bp.route("/admin/dashboard", methods=["GET", "OPTIONS"])
@jwt_required()
@admin_required
def admin_dashboard():
    return AdminRouteHandler.dashboard_stats()


# ================= SYSTEM STATS =================
@admin_bp.route("/admin/stats", methods=["GET", "OPTIONS"])
@jwt_required()
@admin_required
def admin_stats():
    return AdminRouteHandler.dashboard_stats()


# ================= ADMIN REPORTS =================
@admin_bp.route("/admin/reports", methods=["GET", "OPTIONS"])
@jwt_required()
@admin_required
def admin_reports():
    return AdminRouteHandler.all_reports()


@admin_bp.route("/admin/reports/<int:report_id>/approve", methods=["PUT", "OPTIONS"])
@jwt_required()
@admin_required
def approve_report(report_id):
    return AdminRouteHandler.approve_report(report_id)


@admin_bp.route("/admin/reports/<int:report_id>/complete", methods=["PUT", "OPTIONS"])
@jwt_required()
@admin_required
def complete_report(report_id):
    return AdminRouteHandler.complete_report(report_id)


@admin_bp.route("/admin/reports/<int:report_id>/reject", methods=["PUT", "OPTIONS"])
@jwt_required()
@admin_required
def reject_report(report_id):
    return AdminRouteHandler.reject_report(report_id)


@admin_bp.route("/admin/reports/<int:report_id>", methods=["DELETE", "OPTIONS"])
@jwt_required()
@admin_required
def delete_report(report_id):
    return AdminRouteHandler.delete_report(report_id)


# ================= ADMIN PICKUP REQUESTS =================
@admin_bp.route("/admin/requests", methods=["GET", "OPTIONS"])
@jwt_required()
@admin_required
def admin_requests():
    return AdminRouteHandler.all_requests()


@admin_bp.route("/admin/requests/<int:request_id>/approve", methods=["PUT", "OPTIONS"])
@jwt_required()
@admin_required
def approve_request(request_id):
    return AdminRouteHandler.approve_request(request_id)


@admin_bp.route("/admin/requests/<int:request_id>/complete", methods=["PUT", "OPTIONS"])
@jwt_required()
@admin_required
def complete_request(request_id):
    return AdminRouteHandler.complete_request(request_id)


@admin_bp.route("/admin/requests/<int:request_id>/reject", methods=["PUT", "OPTIONS"])
@jwt_required()
@admin_required
def reject_request(request_id):
    return AdminRouteHandler.reject_request(request_id)


@admin_bp.route("/admin/requests/<int:request_id>", methods=["DELETE", "OPTIONS"])
@jwt_required()
@admin_required
def delete_request(request_id):
    return AdminRouteHandler.delete_completed_request(request_id)

 