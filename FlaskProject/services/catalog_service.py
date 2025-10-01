from flask import flash

class Products():
    def __init__(self, product_id, name, color, sizes, price, stock, image_url, category):
        self.product_id = product_id
        self.name = name
        self.color = color
        self.sizes = sizes
        self.price = price
        self.stock = stock
        self.image_url = image_url
        self.category = category

    def add_product(self):
        added_data = {
            "id": len(products) + 1,
            "name": self.name,
            "color": self.color,
            "sizes": self.sizes,
            "price": self.price,
            "stock": self.stock,
            "category": self.category
        }
        products.append(added_data)

class Trainers(Products):
    def __init__(self, product_id, name, color, sizes, price, stock, image_url):
        super().__init__(product_id, name, color, sizes, price, stock, image_url, category="Mаратонки")


class Boots(Products):
    def __init__(self, product_id, name, color, sizes, price, stock, image_url):
        super().__init__(product_id, name, color, sizes, price, stock, image_url, category="Боти")


class Formal(Products):
    def __init__(self, product_id, name, color, sizes, price, stock, image_url):
        super().__init__(product_id, name, color, sizes, price, stock, image_url, category="Официални")


class Sneakers(Products):
    def __init__(self, product_id, name, color, sizes, price, stock, image_url):
        super().__init__(product_id, name, color, sizes, price, stock, image_url, category="Кецове")


class Sandals(Products):
    def __init__(self, product_id, name, color, sizes, price, stock, image_url):
        super().__init__(product_id, name, color, sizes, price, stock, image_url, category="Чехли")


products = [
    {"id": 1, "name": "Nike Air Max", "color": "бели", "sizes": ["36", "37", "39"], "price": 120, "stock": 5, "image_url": "/static/images/NikeAirMax.webp", "category": "Маратонки"},
    {"id": 2, "name": "Clara Barson", "color": "черни", "sizes": ["36", "37", "38", "39", "40"], "price": 75, "stock": 20, "image_url": "/static/images/Clara.webp", "category": "Боти"},
    {"id": 3, "name": "Puma RS-X", "color": "черни", "sizes": ["36", "37", "38", "40"], "price": 160, "stock": 2, "image_url": "/static/images/PumaRSX.webp", "category": "Маратонки"},
    {"id": 4, "name": "Lasocki Classic", "color": "кафяви", "sizes": ["37", "39", "41", "42"], "price": 50, "stock": 10, "image_url": "/static/images/lasocki.jpg", "category": "Официални"},
    {"id": 5, "name": "HUGO", "color": "черни", "sizes": ["40", "41", "42", "43"], "price": 300, "stock": 20, "image_url": "/static/images/Hugo.webp", "category": "Боти"},
    {"id": 6, "name": "Guess Heels", "color": "червени", "sizes": ["36", "37", "38", "39"], "price": 400, "stock": 1, "image_url": "/static/images/GuessHeels.jpg", "category": "Официални"},
    {"id": 7, "name": "Adidas Ultraboost", "color": "сини", "sizes": ["38", "39", "40", "41"], "price": 125, "stock": 8, "image_url": "/static/images/Adidas.avif", "category": "Маратонки"},
    {"id": 8, "name": "Timberland Boots", "color": "кафяви", "sizes": ["40", "41", "42", "43"], "price": 120, "stock": 4, "image_url": "/static/images/Timberland.jpg", "category": "Боти"},
    {"id": 9, "name": "Converse All Star", "color": "черни", "sizes": ["36", "37", "38", "39", "40"], "price": 100, "stock": 15, "image_url": "/static/images/Converse.webp", "category": "Кецове"},
    {"id": 10, "name": "Beverly Hills Polo Club ", "color": "розови", "sizes": ["37", "38", "39"], "price": 77, "stock": 12, "image_url": "/static/images/Polo.webp", "category": "Кецове"},
    {"id": 11, "name": "Steve Madden Pumps", "color": "бежави", "sizes": ["36", "37", "38"], "price": 71, "stock": 3, "image_url": "/static/images/SteveMadden.jpg", "category": "Официални"},
    {"id": 12, "name": "EA7 Emporio Armani", "color": "розови", "sizes": ["36", "37", "38", "39"], "price": 75, "stock": 19, "image_url": "/static/images/ЕА7.webp", "category": "Чехли"},
    {"id": 12, "name": "Nike", "color": "черни", "sizes": ["39", "40", "41"], "price": 55, "stock": 23, "image_url": "/static/images/NikeOne.webp", "category": "Чехли"},

]

def get_product(product_id):
    for product in products:
        if product_id == product["id"]:
            return product
    flash("Продуктът не е открит!", "danger")
    return None


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


def filter_products(product_list, max_price=None, available_size=None, in_stock=False, category=None):
    result = product_list.copy()

    if max_price:
        result = list(filter(lambda p: p["price"] <= max_price, result))

    if available_size:
        result = list(filter(lambda p: available_size in p["sizes"], result))

    if in_stock:
        result = list(filter(lambda p: p["stock"] > 0, result))

    if category and category != "all":
        result = list(filter(lambda p: p["category"] == category, result))

    return result

def get_categories():
    categories = set()
    for product in products:
        categories.add(product["category"])
    return sorted(list(categories))
