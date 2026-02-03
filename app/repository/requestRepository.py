from app.models.request import PickupRequest
from app.extensions import db

class RequestRepository:

    @staticmethod
    def save(req):
        db.session.add(req)
        db.session.commit()

    @staticmethod
    def count_pending(user_id):
        return PickupRequest.query.filter_by(
            user_id=user_id,
            status="pending"
        ).count()

    @staticmethod
    def count_completed(user_id):
        return PickupRequest.query.filter_by(
            user_id=user_id,
            status="completed"
        ).count()
