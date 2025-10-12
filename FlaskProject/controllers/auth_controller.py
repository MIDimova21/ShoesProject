import os

from flask import Blueprint, request, flash, redirect, url_for, render_template, session, current_app
from flask_login import login_user, logout_user, current_user
from werkzeug.utils import secure_filename

from FlaskProject.services.auth_service import User
from FlaskProject import db, login_manager

auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth_bp.route('/', methods=['GET', 'POST'])
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

        if user.check_password(password):
            login_user(user)
            return redirect(url_for("catalog.show_catalog"))
        else:
            flash("Грешен имейл или парола.")


    return render_template("login.html")


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template("profile.html", current_user=current_user)



@auth_bp.route('/upload_picture', methods=['POST'])
def upload_picture():
    if 'profile_picture' not in request.files:
        flash('Няма избран файл')
        return redirect(url_for('auth.profile'))

    file = request.files['profile_picture']
    if file.filename == '':
        flash('Няма избран файл')
        return redirect(url_for('auth.profile'))

    if file:
        filename = secure_filename(f"{current_user.first_name}_pfp.png")
        save_path = os.path.join(current_app.root_path, 'static', 'images', filename)

        file.save(save_path)
        flash('Снимката е променена успешно!')

    return redirect(url_for('auth.profile'))

