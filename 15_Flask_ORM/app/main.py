from flask import Flask

from app.database.database import db, base


def setup_database(app):
    with app.app_context():
        @app.before_first_request
        def create_tables():
            base.metadata.create_all(db)


def create_app():
    app = Flask(__name__)

    setup_database(app)

    from .views.cars import  cars_bp
    from .views.owners import owners_bp
    app.register_blueprint(owners_bp)
    app.register_blueprint(cars_bp)

    return app
