from flask import render_template, redirect, url_for, Blueprint, request, session
from indussh.models import Product

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def index():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')