from flask import Flask

from controllers.catalog_controller import catalog_bp
from controllers.auth_controller import auth_bp


app = Flask(__name__)
app.secret_key = 'W292F'

app.register_blueprint(auth_bp)
app.register_blueprint(catalog_bp)

if __name__ == '__main__':
    app.run()
