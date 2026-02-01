import os
from flask import Flask, send_from_directory
from flask_cors import CORS

from app.extensions import db, bcrypt, jwt
from app.routes.auth_Routes import auth_bp
from app.routes.adminRoutes import admin_bp
from app.routes.reportRoutes import report_bp
from app.routes.requestRoutes import request_bp
from app.routes.dashboardRoutes import dashboard_bp
from app.routes.driver_routes import driver_bp
from app.utils.seed_admin import seed_admin


def create_app():
    app = Flask(__name__)

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
    UPLOAD_FOLDER = os.path.join(ROOT_DIR, "uploads")

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "secret123")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "waste.db")
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "jwt-secret-123")
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_HEADER_NAME"] = "Authorization"
    app.config["JWT_HEADER_TYPE"] = "Bearer"

    frontend_url = os.getenv(
        "FRONTEND_URL",
        "https://waste-management-frontend-kohl.vercel.app"
    )

    CORS(
        app,
        resources={r"/*": {"origins": frontend_url}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    @app.route("/uploads/<path:filename>")
    def serve_uploaded_file(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    app.register_blueprint(auth_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(request_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(driver_bp)

    with app.app_context():
        db.create_all()
        seed_admin()

    return app
