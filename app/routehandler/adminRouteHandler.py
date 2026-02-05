from flask import jsonify, request
from app.models.user import User
from app.models.report import Report
from app.models.request import PickupRequest
from app.extensions import db

from app.utils.task_service import (
    approve_item,
    reject_item,
    complete_item,
    assign_driver
)


class AdminRouteHandler:

    # ================= DASHBOARD =================
    @staticmethod
    def dashboard_stats():
        return jsonify({
            "totalUsers": User.query.count(),

            "totalReports": Report.query.count(),
            "pendingReports": Report.query.filter_by(status="pending").count(),
            "approvedReports": Report.query.filter_by(status="approved").count(),
            "rejectedReports": Report.query.filter_by(status="rejected").count(),
            "completedReports": Report.query.filter_by(status="completed").count(),

            "totalRequests": PickupRequest.query.count(),
            "pendingPickups": PickupRequest.query.filter_by(status="pending").count(),
            "approvedPickups": PickupRequest.query.filter_by(status="approved").count(),
            "rejectedPickups": PickupRequest.query.filter_by(status="rejected").count(),
            "completedPickups": PickupRequest.query.filter_by(status="completed").count(),
        }), 200

    # ================= REPORTS (PAGINATED) =================
    @staticmethod
    def all_reports():
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))

        pagination = Report.query.paginate(
            page=page,
            per_page=limit,
            error_out=False
        )

        reports = pagination.items

        return jsonify({
            "data": [
                {
                    "id": r.id,
                    "issueType": r.issueType,
                    "location": r.location,
                    "status": r.status,
                    "photo": r.photo,
                    "driver": r.driver.name if r.driver else None,
                    "userId": r.user_id
                }
                for r in reports
            ],
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages
        }), 200

    @staticmethod
    def approve_report(report_id):
        report = Report.query.get_or_404(report_id)
        approve_item(report)
        return jsonify({"message": "Report approved"}), 200

    @staticmethod
    def reject_report(report_id):
        report = Report.query.get_or_404(report_id)
        reject_item(report)
        return jsonify({"message": "Report rejected"}), 200

    @staticmethod
    def complete_report(report_id):
        report = Report.query.get_or_404(report_id)
        complete_item(report)
        return jsonify({"message": "Report completed"}), 200

    @staticmethod
    def delete_report(report_id):
        report = Report.query.get_or_404(report_id)
        db.session.delete(report)
        db.session.commit()
        return jsonify({"message": "Report deleted"}), 200

    @staticmethod
    def assign_driver_to_report(report_id):
        driver_id = request.json.get("driver_id")
        if not driver_id:
            return jsonify({"message": "Driver ID required"}), 400

        report = Report.query.get_or_404(report_id)
        try:
            assign_driver(report, driver_id)
        except ValueError as e:
            return jsonify({"message": str(e)}), 400

        return jsonify({"message": "Driver assigned to report"}), 200

    # ================= PICKUP REQUESTS (PAGINATED) =================
    @staticmethod
    def all_requests():
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))

        pagination = PickupRequest.query.paginate(
            page=page,
            per_page=limit,
            error_out=False
        )

        requests = pagination.items

        return jsonify({
            "data": [
                {
                    "id": r.id,
                    "wasteType": r.wasteType,
                    "address": r.address,
                    "date": r.date,
                    "timeSlot": r.timeSlot,
                    "phone": r.phone,
                    "status": r.status,
                    "driver": r.driver.name if r.driver else None,
                    "userId": r.user_id
                }
                for r in requests
            ],
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages
        }), 200

    @staticmethod
    def approve_request(request_id):
        req = PickupRequest.query.get_or_404(request_id)
        approve_item(req)
        return jsonify({"message": "Request approved"}), 200

    @staticmethod
    def reject_request(request_id):
        req = PickupRequest.query.get_or_404(request_id)
        reject_item(req)
        return jsonify({"message": "Request rejected"}), 200

    @staticmethod
    def complete_request(request_id):
        req = PickupRequest.query.get_or_404(request_id)
        complete_item(req)
        return jsonify({"message": "Request completed"}), 200

    @staticmethod
    def delete_completed_request(request_id):
        req = PickupRequest.query.get_or_404(request_id)
        db.session.delete(req)
        db.session.commit()
        return jsonify({"message": "Pickup request deleted"}), 200

    @staticmethod
    def assign_driver_to_request(request_id):
        driver_id = request.json.get("driver_id")
        if not driver_id:
            return jsonify({"message": "Driver ID required"}), 400

        pickup = PickupRequest.query.get_or_404(request_id)
        try:
            assign_driver(pickup, driver_id)
        except ValueError as e:
            return jsonify({"message": str(e)}), 400

        return jsonify({"message": "Driver assigned to pickup"}), 200
