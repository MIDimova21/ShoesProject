from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

calendar_bp = Blueprint('calendar', __name__)

EVENTS = [{'title': 'Nike - зареждане', 'description': 'Air max', 'date': '2025-10-17'}]


@calendar_bp.route("/calendar", methods=["GET"])
@login_required
def calendar():
    return render_template("calendar.html", events=EVENTS)


@calendar_bp.route("/calendar/add", methods=["POST"])
@login_required
def add_event():
    if not current_user.is_admin:
        flash("Нямате права за добавяне на събития!")
        return redirect(url_for('calendar.calendar'))

    title = request.form.get("title")
    description = request.form.get("description", "")
    date = request.form.get("date")

    if not title or not date:
        flash("Моля, попълнете всички задължителни полета!")
        return redirect(url_for('calendar.calendar'))

    EVENTS.append({
        'title': title,
        'description': description,
        'date': date
    })

    print(EVENTS)

    flash(f"Колекцията '{title}' беше добавена успешно!")
    return redirect(url_for('calendar.calendar'))


@calendar_bp.route("/calendar/delete/<int:event_index>", methods=["GET"])
@login_required
def delete_event(event_index):
    if not current_user.is_admin:
        flash("Нямате права за изтриване на събития!")
        return redirect(url_for('calendar.calendar'))

    if 0 <= event_index < len(EVENTS):
        deleted = EVENTS.pop(event_index)
        flash(f"Събитието '{deleted['title']}' беше изтрито!")
    else:
        flash("Събитието не беше намерено!")

    return redirect(url_for('calendar.calendar'))