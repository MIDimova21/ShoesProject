from flask import Blueprint, render_template, redirect, url_for, request, flash, session

from FlaskProject.services import catalog_service, cart_service, order_service

cart_bp = Blueprint("cart", __name__)

@cart_bp.route("/cart")
def show_cart():
    if not session.get('logged_in'):
        flash("Влезте в профила си за да видите вашата количка.")
        return redirect(url_for('auth.login'))

    cart_items = cart_service.get_cart()
    return render_template("cart.html", cart_items=cart_items)

@cart_bp.route("/cart/add/<int:product_id>")
def add_to_cart(product_id):
    if not session.get('logged_in'):
        flash("Влезте във профила си, за да добавите продукти в количката.")
        return redirect(url_for('auth.login'))

    size = request.form.get('size')

    if not size:
        flash("Моля, изберете размер!")
        return redirect(url_for('catalog.show_catalog'))

    products = catalog_service.get_all_products()
    product = next((p for p in products if p["id"] == product_id), None)

    if product:
        cart_service.add_to_cart(product, size)
        flash(f"{product['name']} (Размер {size}) добавен към количката!")

    return redirect(url_for("catalog.show_catalog"))


@cart_bp.route("/checkout", methods=["GET", "POST"])
def checkout():
    if not session.get('logged_in'):
        flash("Please login to checkout.")
        return redirect(url_for('auth.login'))

    if request.method == "POST":
        address = request.form["address"]
        payment = request.form["payment"]

        order = order_service.create_order(address, payment)
        if order:
            flash("Успешна поръчка!")
            return redirect(url_for("catalog.show_catalog"))
        else:
            flash("Количката ви е празна.")

    return render_template("checkout.html")
