from indussh import db, login_manager
from flask import current_app
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# UserMixin is a class that we need to inherit so that we do not need to implement it's methods and use it's default methods
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True, nullable=False)
    image_file = db.Column(db.String(20), default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(500), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    postcode = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    phone_number = db.Column(db.String(20))

    orders = db.relationship('Order', backref='customer')


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_no = db.Column(db.String(10), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(25), nullable=False)
    category = db.Column(db.String(25), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    minimum_price = db.Column(db.Integer, nullable=False)
    image_file = db.Column(db.String(30), nullable=False,
                           default='default.jpg')
    size_sm = db.Column(db.Integer, nullable=False)
    size_md = db.Column(db.Integer, nullable=False)
    size_l = db.Column(db.Integer, nullable=False)
    size_xl = db.Column(db.Integer, nullable=False)
    added_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    ordered_items = db.relationship('OrderItem', backref='ordered-products')

    def __repr__(self):
        return f"Product('{self.article_no}', '{self.name}', '{self.price}')"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    date_completed = db.Column(db.DateTime)

    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customer.id'), nullable=False)
    order_items = db.relationship('OrderItem', backref='order')

    notes = db.Column(db.Text)

    def __repr__(self):
        return f"Order('{self.id}', '{self.completed}', '{self.amount}')"


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    discounted_price = db.Column(db.Integer, nullable=False)

    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)

    def __repr__(self):
        return f"OrderItem('{self.id}', '{self.quantity}', '{self.discounted_price}')"
