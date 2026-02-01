from datetime import datetime
from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from app.models.report import Report
from app.models.request import PickupRequest
from app.extensions import db

def minutes_ago(dt):
    diff = datetime.utcnow() - dt
    mins = int(diff.total_seconds() / 60)
    return "just now" if mins <= 0 else f"{mins} min ago"

class DashboardRouteHandler:

    @staticmethod
    def get_stats():

        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({"message": "Unauthorized"}), 401

        user_id = int(user_id)

        pending_reports = Report.query.filter_by(
            user_id=user_id, status="pending"
        ).count()

        pending_pickups = PickupRequest.query.filter_by(
            user_id=user_id, status="pending"
        ).count()

        notifications = []

        # ✅ REPORT notifications
        reports = Report.query.filter_by(
            user_id=user_id, notification_sent=False
        ).filter(Report.status.in_(["completed", "rejected"])).all()

        for r in reports:
            msg = (
                f"✅ Your waste report at {r.location} has been completed"
                if r.status == "completed"
                else f"❌ Your waste report at {r.location} was rejected"
            )
            notifications.append(f"{msg} ({minutes_ago(r.updated_at)})")
            r.notification_sent = True

        # ✅ PICKUP notifications
        pickups = PickupRequest.query.filter_by(
            user_id=user_id, notification_sent=False
        ).filter(PickupRequest.status.in_(["completed", "rejected"])).all()

        for p in pickups:
            msg = (
                f"Your pickup request on {p.date} has been completed"
                if p.status == "completed"
                else f"Your pickup request on {p.date} was rejected"
            )
            notifications.append(f"{msg} ({minutes_ago(p.updated_at)})")
            p.notification_sent = True

        db.session.commit()

        return jsonify({
            "pendingReports": pending_reports,
            "pendingRequests": pending_pickups,
            "notifications": notifications
        }), 200
