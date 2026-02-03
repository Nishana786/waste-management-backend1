from flask import Blueprint, request, jsonify

from app.routehandler.userRouteHandler import UserRouteHandler

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    response, status = UserRouteHandler.register_user(data)
    return jsonify(response), status

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    response, status = UserRouteHandler.login_user(data)
    return jsonify(response), status

@auth_bp.route("/users", methods=["GET"])
def get_users():
    users, status = UserRouteHandler.get_all_users()
    return jsonify(users), status

@auth_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    response, status = UserRouteHandler.get_user_by_id(user_id)
    return jsonify(response), status

@auth_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    response, status = UserRouteHandler.update_user(user_id, data)
    return jsonify(response), status

@auth_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    response, status = UserRouteHandler.delete_user(user_id)
    return jsonify(response), status
