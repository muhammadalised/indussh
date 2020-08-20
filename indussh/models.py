from indussh import db, login_manager
from flask import current_app
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_no = db.Column(db.String(20), nullable=False, unique=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(25), nullable=False)
    category = db.Column(db.String(25), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    minimum_price = db.Column(db.Integer, nullable=False)
    image_file = db.Column(db.String(30), nullable=False, default='default.jpg')
    added_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    product_stock = db.relationship('ProductStock', backref='product', lazy=True)

    def __repr__(self):
        return f"Product('{self.article_no}', '{self.title}', '{self.price}')"

class ProductStock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_no = db.Column(db.String(20), db.ForeignKey('product.article_no'))
    small = db.Column(db.Integer, nullable=False)
    medium = db.Column(db.Integer, nullable=False)
    large = db.Column(db.Integer, nullable=False)
    xlarge = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"ProductStock('{self.article_no}', '{self.small}', '{self.medium}')"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_status = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    customer = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    order_item = db.relationship('OrderItem', backref='item', lazy=True)

    def __repr__(self):
        return f"Order('{self.id}', '{self.order_status}', '{self.amount}')"

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    discounted_price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"OrderItem('{self.id}', '{self.item}', '{self.discounted_price}')"

