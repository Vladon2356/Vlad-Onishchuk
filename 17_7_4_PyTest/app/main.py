from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from .database.database import db, base

def setup_database(app):
    with app.app_context():
        @app.before_first_request
        def create_tables():
            base.metadata.create_all(db)


def setup_jwt(app):
    jwt = JWTManager(app)

    from app.models import RevokedTokenModel

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        return RevokedTokenModel.is_jti_blacklisted(jti)


def create_app(config= Config):
    app = Flask(__name__)
    app.config.from_object(config)

    setup_database(app)
    setup_jwt(app)

    from .views.users import users_bp
    from .views.auth import  auth_bp
    from .views.posts import posts_bp
    app.register_blueprint(users_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp)

    return app
