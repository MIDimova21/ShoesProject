from werkzeug.security import generate_password_hash, check_password_hash
from FlaskProject import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(80), unique=True, nullable=False)
    __password = db.Column('password', db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_picture_approved = db.Column(db.Boolean, default=False)

    def get_id(self):
        return str(self.user_id)

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.__password, password)

