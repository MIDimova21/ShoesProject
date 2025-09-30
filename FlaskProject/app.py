from flask import Flask

from controllers.cart_controller import cart_bp
from controllers.catalog_controller import catalog_bp
from controllers.auth_controller import auth_bp
from controllers.admin_controller import admin_bp

app = Flask(__name__)
app.secret_key = 'W292F'

app.register_blueprint(auth_bp)
app.register_blueprint(catalog_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    app.run()
