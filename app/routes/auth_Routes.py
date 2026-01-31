from flask import Blueprint, request, jsonify
from flask_cors import CORS
from app.routehandler.userRouteHandler import UserRouteHandler
from app.extensions import bcrypt, db
from app.models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# 🔥 ENABLE CORS FOR AUTH ROUTES
CORS(auth_bp)

# 🔐 REGISTER USER
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    response, status = UserRouteHandler.register_user(data)
    return jsonify(response), status


# 🔑 LOGIN USER
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    response, status = UserRouteHandler.login_user(data)
    return jsonify(response), status


# 📥 GET ALL USERS
@auth_bp.route("/users", methods=["GET"])
def get_users():
    users, status = UserRouteHandler.get_all_users()
    return jsonify(users), status


# 👤 GET SINGLE USER
@auth_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    response, status = UserRouteHandler.get_user_by_id(user_id)
    return jsonify(response), status


# ✏️ UPDATE USER
@auth_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    response, status = UserRouteHandler.update_user(user_id, data)
    return jsonify(response), status


# 🗑️ DELETE USER
@auth_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    response, status = UserRouteHandler.delete_user(user_id)
    return jsonify(response), status


# 👑 CREATE ADMIN
@auth_bp.route("/create-admin", methods=["POST"])
def create_admin():
    admin = User.query.filter_by(email="admin@gmail.com").first()
    if admin:
        return jsonify({"message": "Admin already exists"}), 200

    admin = User(
        name="Admin",
        email="admin@gmail.com",
        password=bcrypt.generate_password_hash("admin123").decode("utf-8"),
        role="admin"
    )
    db.session.add(admin)
    db.session.commit()

    return jsonify({"message": "Admin created successfully"}), 201
