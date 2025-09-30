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
        product_check = None
        for product in catalog_service.products:
            if product["id"] == item["id"]:
                product_check = product
                break
        if product_check and product_check["stock"] > 0:
            product_check["stock"] -= 1

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
