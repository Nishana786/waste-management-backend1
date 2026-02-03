from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.models.request import PickupRequest
from app.repository.requestRepository import RequestRepository

class RequestRouteHandler:

    @staticmethod
    def create_request():
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({"message": "Unauthorized"}), 401

        data = request.get_json()
        if not data:
            return jsonify({"message": "Invalid request"}), 400

        required_fields = ["address", "wasteType", "date", "timeSlot", "phone"]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"message": f"{field} required"}), 400

        req = PickupRequest(
            address=data["address"],
            wasteType=data["wasteType"],
            date=data["date"],
            timeSlot=data["timeSlot"],
            phone=data["phone"],
            user_id=int(user_id),
            status="pending"
        )

        RequestRepository.save(req)
        return jsonify({"message": "Pickup request submitted"}), 201
