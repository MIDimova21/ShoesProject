from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from FlaskProject.services import catalog_service
from FlaskProject.services.catalog_service import Trainers, Boots, Formal, Sneakers, Sandals

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(f):

    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash("Please login first.")
            return redirect(url_for('auth.login'))

        if not session.get('is_admin'):
            flash("Admin access required.")
            return redirect(url_for('catalog.show_catalog'))

        return f(*args, **kwargs)

    decorated_function.__name__ = f.__name__
    return decorated_function


@admin_bp.route("/products")
@admin_required
def manage_products():
    products = catalog_service.get_all_products()
    return render_template("admin_products.html", products=products)


@admin_bp.route("/products/add", methods=["GET", "POST"])
@admin_required
def add_product():
    if request.method == "POST":
        sizes = request.form["sizes"].split(",")
        sizes = [s.strip() for s in sizes]
        id = len(catalog_service.products) + 1
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

    categories = catalog_service.get_categories()
    return render_template("admin_add_product.html", categories=categories)


@admin_bp.route("/products/edit/<int:product_id>", methods=["GET", "POST"])
@admin_required
def edit_product(product_id):
    product = catalog_service.get_product(product_id)

    if not product:
        flash("Продуктът не е открит!")
        return redirect(url_for("admin.manage_products"))

    if request.method == "POST":
        sizes = request.form["sizes"].split(",")
        sizes = [s.strip() for s in sizes]

        catalog_service.update_product(
            product_id,
            name=request.form["name"],
            color=request.form["color"],
            sizes=sizes,
            price=int(request.form["price"]),
            stock=int(request.form["stock"]),
            category=request.form["category"]
        )
        flash(f"Product updated successfully!")
        return redirect(url_for("admin.manage_products"))

    categories = catalog_service.get_categories()
    return render_template("admin_edit_product.html", product=product, categories=categories)


@admin_bp.route("/products/delete/<int:product_id>")
@admin_required
def delete_product(product_id):
    product = catalog_service.get_product(product_id)
    if product:
        catalog_service.delete_product(product_id)
        flash(f"Product {product['name']} deleted successfully!")
    else:
        flash("Product not found!")

    return redirect(url_for("admin.manage_products"))

