# 🔹 JWT token create cheyyan
from flask_jwt_extended import create_access_token

from app.models.user import User
from app.extensions import bcrypt
from app.repository.userRepository import UserRepository


class UserRouteHandler:
   

    # =====================================================
    # 🔐 REGISTER USER
    # =====================================================
    @staticmethod
    def register_user(data):
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return {"message": "All fields required"}, 400

        existing_user = UserRepository.find_by_email(email)
        if existing_user:
            return {"message": "Email already exists"}, 400

        
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        UserRepository.create_user(
            name=name,
            email=email,
            hashed_password=hashed_password
        )

        return {"message": "User registered successfully"}, 201

    # =====================================================
    #  GET ALL USERS
    # =====================================================
    @staticmethod
    def get_all_users():
        users = UserRepository.find_all()
        result = []

        for user in users:
            result.append({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            })

        return result, 200

    # =====================================================
    # 👤 GET SINGLE USER
    # =====================================================
    @staticmethod
    def get_user_by_id(user_id):
        user = UserRepository.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }, 200

    # =====================================================
    # ✏️ UPDATE USER
    # =====================================================
    @staticmethod
    def update_user(user_id, data):
        user = UserRepository.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404

        name = data.get("name")
        email = data.get("email")
        role = data.get("role") 

        UserRepository.update_user(
            user,
            name=name,
            email=email,
            role=role
        )

        return {"message": "User updated successfully"}, 200

    # =====================================================
    # ❌ DELETE USER
    # =====================================================
    @staticmethod
    def delete_user(user_id):
        user = UserRepository.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404

        UserRepository.delete_user(user)
        return {"message": "User deleted successfully"}, 200

       # =====================================================
    # 🔐 LOGIN USER 
    # =====================================================
    @staticmethod
    def login_user(data):
        email = data.get("email")
        password = data.get("password")

        user = UserRepository.find_by_email(email)

        if not user:
            return {"message": "Invalid credentials"}, 401

        if not bcrypt.check_password_hash(user.password, password):
            return {"message": "Invalid credentials"}, 401

    
        access_token = create_access_token(
            identity=str(user.id),          
            additional_claims={"role": user.role}
        )

        return {
            "access_token": access_token,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            }
        }, 200
