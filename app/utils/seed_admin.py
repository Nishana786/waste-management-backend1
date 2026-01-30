import os
from app.extensions import db, bcrypt
from app.models.user import User

def seed_admin():
    email = os.getenv("ADMIN_EMAIL", "admin@gmail.com")
    password = os.getenv("ADMIN_PASSWORD", "admin123")

    admin = User.query.filter_by(role="admin").first()

    if not admin:
        admin = User(
            name="Super Admin",
            email=email,
            role="admin",
            password=bcrypt.generate_password_hash(password).decode("utf-8")
        )
        db.session.add(admin)
        db.session.commit()
