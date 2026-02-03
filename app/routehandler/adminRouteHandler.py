from flask import jsonify
from datetime import datetime
from app.models.user import User
from app.models.report import Report
from app.models.request import PickupRequest
from app.extensions import db


class AdminRouteHandler:

    # ================= DASHBOARD STATS =================
    @staticmethod
    def dashboard_stats():
        return jsonify({

            # USERS
            "totalUsers": User.query.count(),

            # REPORTS
            "totalReports": Report.query.count(),
            "pendingReports": Report.query.filter_by(status="pending").count(),
            "approvedReports": Report.query.filter_by(status="approved").count(),
            "rejectedReports": Report.query.filter_by(status="rejected").count(),
            "completedReports": Report.query.filter_by(status="completed").count(),

            # PICKUP REQUESTS
            "totalRequests": PickupRequest.query.count(),
            "pendingPickups": PickupRequest.query.filter_by(status="pending").count(),
            "approvedPickups": PickupRequest.query.filter_by(status="approved").count(),
            "rejectedPickups": PickupRequest.query.filter_by(status="rejected").count(),
            "completedPickups": PickupRequest.query.filter_by(status="completed").count(),

        }), 200


    # ================= REPORTS (ALL USERS) =================
    @staticmethod
    def all_reports():
        reports = Report.query.all()

        return jsonify([
            {
                "id": r.id,
                "issueType": r.issueType,
                "location": r.location,
                "status": r.status,
                "photo": r.photo,
                "userId": r.user_id
            }
            for r in reports
        ]), 200


    @staticmethod
    def approve_report(report_id):
        report = Report.query.get_or_404(report_id)
        report.status = "approved"
        db.session.commit()
        return jsonify({"message": "Report approved"}), 200


    @staticmethod
    def complete_report(report_id):
        report = Report.query.get_or_404(report_id)
        report.status = "completed"
        db.session.commit()
        return jsonify({"message": "Report completed"}), 200


    @staticmethod
    def reject_report(report_id):
        report = Report.query.get_or_404(report_id)
        report.status = "rejected"
        db.session.commit()
        return jsonify({"message": "Report rejected"}), 200


    @staticmethod
    def delete_report(report_id):
        report = Report.query.get_or_404(report_id)
        db.session.delete(report)
        db.session.commit()
        return jsonify({"message": "Report deleted"}), 200


    # ================= PICKUP REQUESTS (ALL USERS) =================
    @staticmethod
    def all_requests():
        requests = PickupRequest.query.all()

        return jsonify([
            {
                "id": r.id,
                "wasteType": r.wasteType,
                "address": r.address,
                "date": r.date,
                "timeSlot": r.timeSlot,
                "phone": r.phone,
                "status": r.status,
                "userId": r.user_id
            }
            for r in requests
        ]), 200


    @staticmethod
    def approve_request(request_id):
        req = PickupRequest.query.get_or_404(request_id)
        req.status = "approved"
        db.session.commit()
        return jsonify({"message": "Request approved"}), 200


    @staticmethod
    def complete_request(request_id):
        req = PickupRequest.query.get_or_404(request_id)
        req.status = "completed"
        db.session.commit()
        return jsonify({"message": "Request completed"}), 200


    @staticmethod
    def reject_request(request_id):
        req = PickupRequest.query.get_or_404(request_id)
        req.status = "rejected"
        db.session.commit()
        return jsonify({"message": "Request rejected"}), 200


    @staticmethod
    def delete_completed_request(request_id):
        req = PickupRequest.query.get_or_404(request_id)
        db.session.delete(req)
        db.session.commit()
        return jsonify({"message": "Pickup request deleted"}), 200
