from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import current_user, login_required

from FlaskProject.services.catalog_service import Products
from FlaskProject.services import cart_service, order_service

cart_bp = Blueprint("cart", __name__)

@cart_bp.route("/cart")
@login_required
def show_cart():
    cart_items = cart_service.get_cart()

    products_in_cart = []
    for item in cart_items:
        product = Products.query.get(item["product_id"])
        if product:
            products_in_cart.append({
                "product": product,
                "size": item["size"],
                "quantity": item.get("quantity", 1)
            })

    return render_template("cart.html", cart_items=products_in_cart)

@cart_bp.route("/cart/add/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id):
    size = request.form.get("size")
    if not size:
        flash("Моля, изберете размер!")
        return redirect(url_for("catalog.show_catalog"))

    product = Products.query.get(product_id)
    if not product:
        flash("Продуктът не съществува.")
        return redirect(url_for("catalog.show_catalog"))

    cart_service.add_to_cart(product.product_id, size)

    return redirect(url_for("catalog.show_catalog"))

@cart_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    if request.method == "POST":
        address = request.form.get("address")
        payment = request.form.get("payment")

        order = order_service.create_order(current_user.user_id, address, payment)
        if order:
            flash("Успешна поръчка!")
            return redirect(url_for("catalog.show_catalog"))
        else:
            flash("Количката ви е празна или продуктите нямат наличност.")

    return render_template("checkout.html")