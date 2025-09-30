from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from FlaskProject.services import catalog_service

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
        product_data = {
            "id": len(catalog_service.products) + 1,
            "name": request.form["name"],
            "color": request.form["color"],
            "sizes": request.form["sizes"],
            "price": int(request.form["price"]),
            "stock": int(request.form["stock"])
        }
        catalog_service.products.append(product_data)
        flash(f"Product {product_data['name']} added successfully!")
        return redirect(url_for("admin.manage_products"))

    return render_template("admin_add_product.html")


@admin_bp.route("/products/edit/<int:product_id>", methods=["GET", "POST"])
@admin_required
def edit_product(product_id):
    product = catalog_service.get_product(product_id)

    if not product:
        flash("Product not found!")
        return redirect(url_for("admin.manage_products"))

    if request.method == "POST":
        catalog_service.update_product(
            product_id,
            name=request.form["name"],
            color=request.form["color"],
            sizes=request.form["sizes"],
            price=int(request.form["price"]),
            stock=int(request.form["stock"])
        )
        flash(f"Product updated successfully!")
        return redirect(url_for("admin.manage_products"))

    return render_template("admin_edit_product.html", product=product)


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

