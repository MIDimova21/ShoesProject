from flask import session

def add_to_cart(product_id, size, quantity=1):
    if "cart" not in session:
        session["cart"] = []

    # Check if product with same id and size already in cart
    for item in session["cart"]:
        if item["product_id"] == product_id and item["size"] == size:
            item["quantity"] += quantity
            session.modified = True
            return

    # Add new item
    session["cart"].append({
        "product_id": product_id,
        "size": size,
        "quantity": quantity
    })
    session.modified = True

def get_cart():
    return session.get("cart", [])
