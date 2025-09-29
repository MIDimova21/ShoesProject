from flask import session
from FlaskProject.services import catalog_service

class Order:
    def __init__(self, address, payment_method):
        self.address = address,
        self.payment_method = payment_method

orders = []

def create_order(address, payment_method):
    cart = session.get("cart", [])
    if not cart:
        return None

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

    session["cart"] = []
    session.modified = True

    return order

def get_orders():
    return orders
