from FlaskProject import db
from FlaskProject.services.catalog_service import Products
from flask import session


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    address = db.Column(db.String(200))
    payment_method = db.Column(db.String(50))
    items = db.relationship("OrderItem", back_populates="order")
    user = db.relationship("User", backref="orders")


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.product_id"), nullable=False)
    size = db.Column(db.String(5))
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Integer)

    order = db.relationship("Order", back_populates="items")
    product = db.relationship("Products", back_populates="order_items")


def create_order(user_id, address, payment_method):
    cart = session.get("cart", [])
    if not cart:
        return None

    order = Order(user_id=user_id, address=address, payment_method=payment_method)
    db.session.add(order)
    db.session.flush()

    for item in cart:
        product = Products.query.get(item["product_id"])
        if not product or product.stock <= 0:
            continue

        quantity = item.get("quantity", 1)
        if product.stock < quantity:
            continue

        product.stock -= quantity
        db.session.add(product)

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.product_id,
            size=item["size"],
            quantity=quantity,
            price=product.price
        )
        db.session.add(order_item)

    db.session.commit()

    # Clear cart after successful order
    session["cart"] = []
    session.modified = True

    return order
