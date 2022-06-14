from indussh import db, login_manager

from flask import current_app
from flask_login import UserMixin
from datetime import datetime
import pandas as pd

from werkzeug.security import generate_password_hash, check_password_hash

# class Role(db.Model):
#     __tablename__ = 'roles'
#     pass

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# UserMixin is a class that we need to inherit so that we do not need to implement it's methods and use it's default methods
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True, nullable=False)
    image_file = db.Column(db.String(20), default='default.jpg')
    password_hash = db.Column(db.String(128), nullable=False)
    
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(self.password_hash, password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(500), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    postcode = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    phone_number = db.Column(db.String(20))

    orders = db.relationship('Order', backref='customer')


class Product(db.Model):
    __tablename__ = 'products'

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

    ordered_items = db.relationship('OrderItem', backref='ordered_products')

    def __repr__(self):
        return f"Product('{self.article_no}', '{self.name}', '{self.price}')"
    
    @staticmethod
    def insert_products():
        columns = [
        'article_no', 'name', 'description', 'type', 'category', 
        'price', 'minimum_price', 'image_file', 'size_sm', 'size_md',
        'size_l', 'size_xl'
        ]

        df = pd.read_csv(current_app.config['PRODUCTS_DATA_PATH'])
        df.columns = columns

        for i in range(len(df)):
            product = Product(
                article_no=str(df.iloc[i]['article_no']),
                name=df.iloc[i]['name'],
                description=df.iloc[i]['description'],
                type=df.iloc[i]['type'],
                category=df.iloc[i]['category'],
                price=int(df.iloc[i]['price']),
                minimum_price=int(df.iloc[i]['minimum_price']),
                image_file=df.iloc[i]['image_file'],
                size_sm=int(df.iloc[i]['size_sm']),
                size_md=int(df.iloc[i]['size_md']),
                size_l=int(df.iloc[i]['size_l']),
                size_xl=int(df.iloc[i]['size_xl'])
            )

            db.session.add(product)
        db.session.commit()
        print(f'{len(df)} Products Seeded into Database!')


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    date_completed = db.Column(db.DateTime)

    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    order_items = db.relationship('OrderItem', backref='order')

    notes = db.Column(db.Text)

    def __repr__(self):
        return f"Order('{self.id}', '{self.completed}', '{self.amount}')"


class OrderItem(db.Model):
    __tablename__ = 'orderitems'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    discounted_price = db.Column(db.Integer, nullable=False)

    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)

    def __repr__(self):
        return f"OrderItem('{self.id}', '{self.quantity}', '{self.discounted_price}')"
