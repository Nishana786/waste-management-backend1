from datetime import datetime
from app.extensions import db

class PickupRequest(db.Model):
    __tablename__ = "pickup_requests"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.Text, nullable=False)
    wasteType = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    timeSlot = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    status = db.Column(db.String(50), default="pending")
    user_id = db.Column(db.Integer)

    driver_id = db.Column(
        db.Integer,
        db.ForeignKey("drivers.id"),  
        nullable=True
    )

    driver = db.relationship("Driver", backref="pickups")

    notification_sent = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
