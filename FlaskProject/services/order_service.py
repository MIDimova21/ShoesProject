# services/order_service.py
from flask import session
from FlaskProject.services import catalog_service

orders = []  # keep all orders in memory

def create_order(address, payment_method):
    cart = session.get("cart", [])
    if not cart:
        return None  # no items to order

    # reduce stock
    for item in cart:
        product = next((p for p in catalog_service.products if p["id"] == item["id"]), None)
        if product and product["stock"] > 0:
            product["stock"] -= 1

    order = {
        "id": len(orders) + 1,
        "items": cart.copy(),
        "address": address,
        "payment": payment_method,
    }
    orders.append(order)

    # empty cart
    session["cart"] = []
    session.modified = True

    return order

def get_orders():
    return orders
