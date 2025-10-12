from flask import Blueprint, render_template, request
from flask_login import current_user

from FlaskProject.services.catalog_service import Products

catalog_bp = Blueprint('catalog', __name__)

@catalog_bp.route("/")
def show_catalog():
    query = request.args.get("query")
    max_price = request.args.get("max_price", type=int)
    available_size = request.args.get("available_size")
    in_stock = request.args.get("in_stock") == "on"
    category = request.args.get("category")

    products = get_filtered_products(query, max_price, available_size, in_stock, category)
    categories = list({product.category for product in Products.query.all() if product.category})

    return render_template(
        "catalog.html",
        products=products,
        search_query=query,
        max_price=max_price,
        in_stock=in_stock,
        categories=categories,
        selected_category=category,
        current_user=current_user
    )


@catalog_bp.route("/filter", methods=['GET', 'POST'])
def get_filtered_products(query=None, max_price=None, available_size=None, in_stock=False, category=None):
    products_query = Products.query

    if query:
        q = f"%{query.lower()}%"
        products_query = products_query.filter(
            Products.name.ilike(q) | Products.color.ilike(q)
        )

    if max_price is not None:
        products_query = products_query.filter(Products.price <= max_price)

    if in_stock:
        products_query = products_query.filter(Products.stock > 0)

    if category and category.lower() != "all":
        products_query = products_query.filter(Products.category == category)

    products = products_query.all()

    if available_size:
        filtered_products = []
        for p in products:
            if p.sizes:
                sizes_list = [s for s in p.sizes.split(",")]
                if available_size in sizes_list:
                    filtered_products.append(p)
        products = filtered_products

    return products
