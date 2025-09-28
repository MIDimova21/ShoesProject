products = [
    {"id": 1, "name": "Sneakers", "color": "white", "sizes": "36, 37, 39", "price": 60, "stock": 5},
    {"id": 2, "name": "Boots", "color": "black", "sizes": "36, 37, 38, 40", "price": 80, "stock": 2},
    {"id": 3, "name": "Sandals", "color": "brown",  "sizes": "37, 39, 41, 42", "price": 40, "stock": 10},
]

def get_all_products():
    return products

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
