from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):

        # ✅ CORS preflight request allow
        if request.method == "OPTIONS":
            return "", 200

        # ✅ JWT verify first
        verify_jwt_in_request()

        claims = get_jwt()

        if claims.get("role") != "admin":
            return jsonify({"message": "Admin only"}), 403

        return fn(*args, **kwargs)

    return wrapper
