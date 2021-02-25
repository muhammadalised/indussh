from flask import Flask, render_template, session, redirect, url_for, Blueprint

users = Blueprint('users' ,__name__)

@users.route('/register')
def register():
    return render_template('register.html')

