from flask import Blueprint, render_template, redirect, url_for, request, flash
from FlaskProject.services import catalog_service, cart_service, order_service

cart_bp = Blueprint("cart", __name__)

@cart_bp.route("/cart")
def show_cart():
    cart_items = cart_service.get_cart()
    return render_template("cart.html", cart_items=cart_items)

@cart_bp.route("/cart/add/<int:product_id>")
def add_to_cart(product_id):
    products = catalog_service.get_all_products()
    product = next((p for p in products if p["id"] == product_id), None)

    if product:
        cart_service.add_to_cart(product)

    return redirect(url_for("cart.show_cart"))


@cart_bp.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        address = request.form["address"]
        payment = request.form["payment"]

        order = order_service.create_order(address, payment)
        if order:
            flash("Order placed successfully!")
            return redirect(url_for("catalog.show_catalog"))
        else:
            flash("Your cart is empty.")

    return render_template("checkout.html")
