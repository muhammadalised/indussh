from flask import Flask, render_template, session, redirect, url_for, Blueprint
from indussh.users.forms import RegisterForm
from indussh.models import User, Customer

users = Blueprint('users' ,__name__)

@users.route('/register')
def register():
    form = RegisterForm()
    return render_template('register.html', form=form)

