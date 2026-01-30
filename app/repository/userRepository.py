from app.models.user import User
from app.extensions import db


class UserRepository:

    @staticmethod
    def create_user(name, email, hashed_password, role="citizen"):
       
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
       
        return User.query.filter_by(email=email).first()

    @staticmethod
    def find_all():
       
        return User.query.all()

    @staticmethod
    def find_by_id(user_id):
       
        return User.query.get(user_id)

    @staticmethod
    def update_user(user, name=None, email=None, role=None):
        
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
       
   
        db.session.delete(user)
        db.session.commit()
