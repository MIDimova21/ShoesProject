from flask import Blueprint, request, flash, redirect, url_for, render_template

from FlaskProject.services import auth_service

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        if auth_service.register(first_name, last_name, email, password):
            flash("Registered successfully! You can now log in.")
            print(auth_service.users)

            return redirect(url_for("auth.login"))
        else:
            flash("You already have an account.")

    return render_template("register.html")


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if auth_service.login(email, password):
            flash("Logged in.")
            return redirect(url_for("auth.home"))
        else:
            flash("Invalid email or password.")

    return render_template("login.html")

@auth_bp.route('/home')
def home():
    return render_template("index.html")