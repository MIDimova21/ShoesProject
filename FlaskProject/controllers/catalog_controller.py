from flask import Blueprint, render_template

from FlaskProject.services import catalog_service

catalog_bp = Blueprint('catalog', __name__)

@catalog_bp.route('/catalog')
def show_catalog():
    products = catalog_service.get_all_products()
    return render_template('catalog.html', products=products)