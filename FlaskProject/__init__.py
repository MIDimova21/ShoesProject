from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()

def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    """"

    from services import auth_service, catalog_service, order_service, review_service
    with app.app_context():
        db.create_all()"""

    from controllers.cart_controller import cart_bp
    from controllers.catalog_controller import catalog_bp
    from controllers.auth_controller import auth_bp
    from controllers.admin_controller import admin_bp
    from controllers.review_controler import review_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(catalog_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(review_bp)

    return app