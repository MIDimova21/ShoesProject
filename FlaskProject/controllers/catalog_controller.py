from flask import Blueprint, render_template, request

from FlaskProject.services import catalog_service

catalog_bp = Blueprint('catalog', __name__)

@catalog_bp.route("/catalog")
def show_catalog():
    query = request.args.get("query")
    max_price = request.args.get("max_price", type=int)
    in_stock = request.args.get("in_stock") == "on"

    products = catalog_service.filter_products(query, max_price, in_stock)

    return render_template(
        "catalog.html",
        products=products,
        search_query=query,
        max_price=max_price,
        in_stock=in_stock
    )