from flask import session

def add_to_cart(product, size):
    if "cart" not in session:
        session["cart"] = []

    cart_item = product.copy()
    cart_item["selected_size"] = size

    session["cart"].append(cart_item)
    session.modified = True


def get_cart():
    return session.get("cart", [])