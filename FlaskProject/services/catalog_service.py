from flask import flash


class Products:
    def __init__(self, product_id, name, color, sizes, price, stock, image_url):
        self.product_id = product_id
        self.name = name
        self.color = color
        self.sizes = sizes
        self.price = price
        self.stock = stock
        self.image_url = image_url


products = [
    {"id": 1, "name": "Nike", "color": "white", "sizes": "36, 37, 39", "price": 60, "stock": 5, "image_url": "/static/photos/Nike_court.webp"},
    {"id": 2, "name": "Puma", "color": "black", "sizes": "36, 37, 38, 40", "price": 80, "stock": 2},
    {"id": 3, "name": "Lasocki", "color": "brown",  "sizes": "37, 39, 41, 42", "price": 40, "stock": 10},
    {"id": 4, "name": "Guess", "color": "red", "sizes": "36, 37, 38, 39", "price": 50, "stock": 1},
]

def add_product(product):
    products.append({
        "id": product.product.id,
        "name": product.product.name,
        "color": product.product.color,
        "sizes": product.product.sizes,
        "price": product.product.price,
        "stock": product.product.stock,
        "image_url": product.product.image_url
    })

def get_product(product_id):
    for product in products:
        if product_id == product["id"]:
            return product
    flash("Product Not Found!", "danger")


def get_all_products():
    return products


def update_product(product_id, **kwargs):
    product = get_product(product_id)
    if not product:
        return None
    for key, value in kwargs.items():
        if key in product:
            product[key] = value
    return product


def delete_product(product_id):
    product = get_product(product_id)
    if product:
        products.remove(product)



def search_products(query):
    result = []
    if query:
        q = query.lower()
        for product in products:
            name = product["name"].lower()
            color = product["color"].lower()
            if q in name or q in color:
                result.append(product)
        return result
    return products

def filter_products(product_list, max_price, available_size, in_stock):
    result = []

    if max_price:
        for product in products:
            if product["price"] <= max_price:
                result.append(product)
        return result

    if available_size:
        for product in products:
            if available_size in product["sizes"]:
                result.append(product)
        return result

    if in_stock:
        for product in products:
            if product["stock"] > 0:
                result.append(product)
        return result

    return product_list
