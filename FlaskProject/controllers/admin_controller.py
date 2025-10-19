from flask import Blueprint, render_template, redirect, url_for, request, flash
from FlaskProject import db
from FlaskProject.services.auth_service import User

from FlaskProject.services.catalog_service import Products, Trainers, Boots, Formal, Sneakers, Sandals

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")



@admin_bp.route("/products")
def manage_products():
    products = Products.query.all()
    return render_template("admin_products.html", products=products)


@admin_bp.route("/created/orders")
def created_orders():
    return render_template("admin_orders.html")



@admin_bp.route("/products/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        sizes = request.form["sizes"]
        name = request.form["name"]
        color = request.form["color"]
        price = int(request.form["price"])
        stock = int(request.form["stock"])
        image = ""
        category = request.form["category"]

        if category == "Маратонки":
            new_product = Trainers(id, name, color, sizes, price, stock, image)
            new_product.add_product()
        elif category == "Боти":
            new_product = Boots(id, name, color, sizes, price, stock, image)
            new_product.add_product()
        elif category == "Официални":
            new_product = Formal(id, name, color, sizes, price, stock, image)
            new_product.add_product()
        elif category == "Кецове":
            new_product = Sneakers(id, name, color, sizes, price, stock, image)
            new_product.add_product()
        elif category == "Чехли":
            new_product = Sandals(id, name, color, sizes, price, stock, image)
            new_product.add_product()

        flash(f"Продуктът е добавен успешно!")
        return redirect(url_for("admin.manage_products"))

    categories = list({product.category for product in Products.query.all() if product.category})
    return render_template("admin_add_product.html", categories=categories)


@admin_bp.route("/products/edit/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    product = Products.query.get(product_id)

    if not product:
        flash("Продуктът не е открит!")
        return redirect(url_for("admin.manage_products"))

    if request.method == "POST":
        sizes = request.form["sizes"]

        product.name = request.form["name"]
        product.color = request.form["color"]
        product.sizes = sizes
        product.price = int(request.form["price"])
        product.stock = int(request.form["stock"])
        product.category = request.form["category"]

        db.session.commit()

        flash("Продуктът беше обновен успешно!")
        return redirect(url_for("admin.manage_products"))


    categories = list({product.category for product in Products.query.all() if product.category})
    return render_template("admin_edit_product.html", product=product, categories=categories)


@admin_bp.route("/products/delete/<int:product_id>")
def delete_product(product_id):
    product = Products.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
    else:
        flash("Продуктът не беше открит!")

    return redirect(url_for("admin.manage_products"))


@admin_bp.route("user/approve/picture")
def approve_picture():
    users = User.query.all()
    for user in users:
        user.is_picture_approved = True
    db.session.commit()
    return redirect(url_for("admin.manage_products"))

@admin_bp.route("user/reject/picture")
def reject_picture():
    users = User.query.all()
    for user in users:
        user.is_picture_approved = False
    db.session.commit()
    return redirect(url_for("admin.manage_products"))

