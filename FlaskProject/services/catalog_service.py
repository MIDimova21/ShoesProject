from FlaskProject import db

class Products(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    color = db.Column(db.String(80), nullable=False)
    sizes = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(200), unique=True, nullable=False)
    category = db.Column(db.String(80), nullable=False)

    order_items = db.relationship("OrderItem", back_populates="product", cascade="all, delete-orphan")



    def add_product(self):
        product = Products(name=self.name, color=self.color, sizes=self.sizes, price=self.price, stock=self.stock,image_url=self.image_url,category=self.category)
        db.session.add(product)
        db.session.commit()

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

