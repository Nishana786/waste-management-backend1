import os
import uuid
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from werkzeug.utils import secure_filename

from app.models.report import Report
from app.repository.reportRepository import ReportRepository

UPLOAD_FOLDER = "uploads"

class ReportRouteHandler:

    @staticmethod
    def create_report():

        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({"message": "Unauthorized"}), 401

        user_id = int(user_id)

        issue_type = request.form.get("issueType")
        location = request.form.get("location")

        if not issue_type or not location:
            return jsonify({"message": "issueType and location required"}), 400

        photo = request.files.get("photo")
        if not photo or photo.filename == "":
            return jsonify({"message": "Photo is required"}), 400

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        filename = secure_filename(photo.filename)
        unique_name = f"{uuid.uuid4()}_{filename}"
        photo.save(os.path.join(UPLOAD_FOLDER, unique_name))

        # ✅ CHANGE ONLY HERE
        report = Report(
            issueType=issue_type,
            description=request.form.get("description"),
            location=location,
            photo=f"{request.host_url}uploads/{unique_name}",
            user_id=user_id
        )

        ReportRepository.save(report)

        return jsonify({"message": "Report submitted successfully"}), 201
