from flask import Blueprint, request, flash, redirect, url_for, render_template, session
from FlaskProject.services import auth_service

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        password_check = request.form['check_password']

        if password == password_check:
            if auth_service.register(first_name, last_name, email, password, password_check):
                flash("Успешна регистрация!Моля влезте в профила си")
                return redirect(url_for("auth.login"))
            else:
                flash("Вече имате профил с този имейл.")
        else:
            flash("Паролата не съвпада.")

    return render_template("register.html")


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = auth_service.login(email, password)
        if user:
            session['user_email'] = user.email
            session['user_name'] = user.first_name
            session['is_admin'] = user.is_admin
            session['logged_in'] = True

            return redirect(url_for("catalog.show_catalog"))
        else:
            flash("Грешен илейл или парола.")

    return render_template("login.html")

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

