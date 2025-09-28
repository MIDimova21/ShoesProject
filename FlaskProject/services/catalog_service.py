products = [
    {"id": 1, "name": "Sneakers", "color": "white", "price": 60, "stock": 5},
    {"id": 2, "name": "Boots", "color": "black", "price": 80, "stock": 2},
    {"id": 3, "name": "Sandals", "color": "brown", "price": 40, "stock": 10},
]

def get_all_products():
    return products

def search_products(query):
    query = query.lower()
    return [
        product for product in products
        if query in product["name"].lower() or query in product["color"].lower()
    ]

def filter_products(query=None, max_price=None, in_stock=False):
    result = products

    # Search filter
    if query:
        q = query.lower()
        result = [p for p in result if q in p["name"].lower() or q in p["color"].lower()]

    # Price filter
    if max_price:
        result = [p for p in result if p["price"] <= max_price]

    # Stock filter
    if in_stock:
        result = [p for p in result if p["stock"] > 0]

    return result

