from flask import jsonify
from datetime import datetime
from app.models.user import User
from app.models.report import Report
from app.models.request import PickupRequest
from app.extensions import db

class AdminRouteHandler:

    # -------- DASHBOARD --------
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

    # -------- PICKUP REQUESTS (FULL DATA) --------
    @staticmethod
    def all_requests():
        reqs = PickupRequest.query.order_by(PickupRequest.created_at.desc()).all()

        return jsonify([
            {
                "id": r.id,
                "wasteType": r.wasteType,
                "address": r.address,
                "date": r.date,
                "timeSlot": r.timeSlot,
                "phone": r.phone,
                "status": r.status,
                "userId": r.user_id,
                "createdAt": r.created_at,
            }
            for r in reqs
        ]), 200

    @staticmethod
    def approve_request(request_id):
        req = PickupRequest.query.get_or_404(request_id)
        req.status = "approved"
        req.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({"message": "Request approved"}), 200

    @staticmethod
    def complete_request(request_id):
        req = PickupRequest.query.get_or_404(request_id)
        req.status = "completed"
        req.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({"message": "Request completed"}), 200

    @staticmethod
    def reject_request(request_id):
        req = PickupRequest.query.get_or_404(request_id)
        req.status = "rejected"
        req.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({"message": "Request rejected"}), 200

    @staticmethod
    def delete_completed_request(request_id):
        req = PickupRequest.query.get_or_404(request_id)
        db.session.delete(req)
        db.session.commit()
        return jsonify({"message": "Pickup request deleted"}), 200
