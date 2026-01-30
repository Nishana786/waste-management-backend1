from app.models.user import User
from app.extensions import db


class UserRepository:

    @staticmethod
    def create_user(name, email, hashed_password, role="citizen"):
        """
        🔹 New user database-il save cheyyan vendiya function
        """
        user = User(
            name=name,
            email=email,
            password=hashed_password,
            role=role
        )
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def find_by_email(email):
        """
        🔹 given email already database-il undo enn check cheyyan
        """
        return User.query.filter_by(email=email).first()

    @staticmethod
    def find_all():
        """
        🔹 Database-il ninn ellaa users fetch cheyyan
        """
        return User.query.all()

    @staticmethod
    def find_by_id(user_id):
        """
        🔹 user_id vech single user fetch cheyyan
        """
        return User.query.get(user_id)

    @staticmethod
    def update_user(user, name=None, email=None, role=None):
        """
        🔹 user details update cheyyan
        """
        if name:
            user.name = name
        if email:
            user.email = email
        if role:
            user.role = role

        db.session.commit()
        return user

    @staticmethod
    def delete_user(user):
        """
        🔹 user database-il ninn delete cheyyan
        """
        db.session.delete(user)
        db.session.commit()
