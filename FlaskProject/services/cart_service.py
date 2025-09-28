from flask import session

def add_to_cart(product):
    # Initialize cart in session if not exists
    if "cart" not in session:
        session["cart"] = []
    session["cart"].append(product)
    session.modified = True  # tell Flask the session changed

def get_cart():
    return session.get("cart", [])
