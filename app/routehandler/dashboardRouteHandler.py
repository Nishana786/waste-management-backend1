from datetime import datetime
from app.models.report import Report
from app.models.request import PickupRequest
from app.extensions import db


# ⏱️ Time helper
def minutes_ago(dt):
    if not dt:
        return "just now"

    diff = datetime.utcnow() - dt
    mins = int(diff.total_seconds() / 60)
    return "just now" if mins <= 0 else f"{mins} min ago"


class DashboardRouteHandler:

    @staticmethod
    def get_stats(user_id):
        """
        user_id route-il ninnu varum
        JWT ivide use cheyyilla
        """

        user_id = int(user_id)

        # 📊 Pending counts
        pending_reports = Report.query.filter_by(
            user_id=user_id,
            status="pending"
        ).count()

        pending_pickups = PickupRequest.query.filter_by(
            user_id=user_id,
            status="pending"
        ).count()

        notifications = []

        # 🔔 REPORT notifications (completed / rejected)
        reports = Report.query.filter_by(
            user_id=user_id,
            notification_sent=False
        ).filter(
            Report.status.in_(["completed", "rejected"])
        ).all()

        for r in reports:
            if r.status == "completed":
                msg = f"✅ Your waste report at {r.location} has been completed"
            else:
                msg = f"❌ Your waste report at {r.location} was rejected"

            notifications.append(
                f"{msg} ({minutes_ago(r.updated_at)})"
            )

            # mark notification sent
            r.notification_sent = True
            r.updated_at = datetime.utcnow()

        # 🔔 PICKUP notifications (completed / rejected)
        pickups = PickupRequest.query.filter_by(
            user_id=user_id,
            notification_sent=False
        ).filter(
            PickupRequest.status.in_(["completed", "rejected"])
        ).all()

        for p in pickups:
            if p.status == "completed":
                msg = f"Your pickup request on {p.date} has been completed"
            else:
                msg = f"Your pickup request on {p.date} was rejected"

            notifications.append(
                f"{msg} ({minutes_ago(p.updated_at)})"
            )

            # mark notification sent
            p.notification_sent = True
            p.updated_at = datetime.utcnow()

        # 💾 save all updates
        db.session.commit()

        # 📦 response data
        return {
            "pendingReports": pending_reports,
            "pendingRequests": pending_pickups,
            "notifications": notifications
        }
