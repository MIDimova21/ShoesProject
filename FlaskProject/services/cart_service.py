from flask import session

def add_to_cart(product):
    if "cart" not in session:
        session["cart"] = []
    session["cart"].append(product)
    session.modified = True

def get_cart():
    return session.get("cart", [])
