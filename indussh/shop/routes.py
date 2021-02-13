from flask import render_template, redirect, url_for, Blueprint, request

shop = Blueprint('shop', __name__)

@shop.route('/')
@shop.route('/shop')
@shop.route('/home')
def index():
    return render_template('index.html')

@shop.route('/about')
def about():
    return render_template('about.html')

@shop.route('/contact')
def contact():
    return render_template('contact.html')