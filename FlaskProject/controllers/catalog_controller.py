from flask import Blueprint, render_template, request

from FlaskProject.services import catalog_service

catalog_bp = Blueprint('catalog', __name__)

@catalog_bp.route("/")
def show_catalog():
    query = request.args.get("query")
    max_price = request.args.get("max_price", type=int)
    available_size = request.args.get("available_size")
    in_stock = request.args.get("in_stock") == "on"
    category = request.args.get("category")

    search = catalog_service.search_products(query)
    filtered = catalog_service.filter_products(search, max_price, available_size, in_stock, category)
    categories = catalog_service.get_categories()

    return render_template(
        "catalog.html",
        products=filtered,
        search_query=query,
        max_price=max_price,
        in_stock=in_stock,
        categories=categories,
        selected_category=category
    )