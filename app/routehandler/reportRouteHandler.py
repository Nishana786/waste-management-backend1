import os
import uuid
from flask import request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity
from werkzeug.utils import secure_filename

from app.models.report import Report
from app.repository.reportRepository import ReportRepository


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

        #  Upload folder from app config
        upload_folder = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_folder, exist_ok=True)

        #  Safe unique filename
        filename = secure_filename(photo.filename)
        unique_name = f"{uuid.uuid4()}_{filename}"

        #  Save image
        photo.save(os.path.join(upload_folder, unique_name))

        #  FIX: SAVE ONLY FILENAME
        report = Report(
            issueType=issue_type,
            description=request.form.get("description"),
            location=location,
            photo=unique_name,    
            user_id=user_id
        )

        ReportRepository.save(report)

        return jsonify({
            "message": "Report submitted successfully",
            "photo": unique_name
        }), 201
