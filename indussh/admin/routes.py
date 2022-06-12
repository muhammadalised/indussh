from flask import Flask, render_template, session, redirect, url_for, Blueprint
from indussh import db
from indussh.models import User, Product

admin = Blueprint('admin', __name__)

@admin.route('/admin/login')
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    form = LoginForm()
    return render_template('admin/login.html', title='Login', form=form)


@admin.route('/admin/logout')
def admin_logout():
    pass


@admin.route('/admin')
@admin.route('/admin/dashboard')
def admin_dashboard():
    pass
