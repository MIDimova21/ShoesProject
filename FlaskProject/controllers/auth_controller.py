from flask import Blueprint, request, flash, redirect, url_for, render_template, session
from FlaskProject.services.auth_service import User
from FlaskProject import db

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
            user = User(first_name=first_name, last_name=last_name, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            if user:
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

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_email'] = user.email
            session['user_name'] = user.first_name
            print(user.email)
            session['is_admin'] = user.is_admin
            print(user.email)
            session['logged_in'] = True

            return redirect(url_for("catalog.show_catalog"))
        else:
            flash("Грешен имейл или парола.")

    return render_template("login.html")

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

