from app.extensions import bcrypt, db
from app.models.user import User

def seed_admin():
    admin = User.query.filter_by(email="admin@gmail.com").first()
    if not admin:
        admin = User(
            name="Admin",
            email="admin@gmail.com",
            password=bcrypt.generate_password_hash("admin123").decode("utf-8"),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()
