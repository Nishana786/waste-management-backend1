from flask import Blueprint, jsonify
from app.extensions import db, bcrypt
from app.models.user import User

dev_bp = Blueprint("dev", __name__)

@dev_bp.route("/create-admin", methods=["GET"])
def create_admin():
    user = User.query.filter_by(email="admin@gmail.com").first()

    if not user:
        user = User(
            name="Admin",
            email="admin@gmail.com",
            role="admin",
            password=bcrypt.generate_password_hash("admin123").decode("utf-8")
        )
        db.session.add(user)
    else:
        user.password = bcrypt.generate_password_hash("admin123").decode("utf-8")
        user.role = "admin"

    db.session.commit()
    return jsonify({"message": "Admin created / reset successfully"}), 200
