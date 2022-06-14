from flask import Flask, render_template, redirect, url_for, Blueprint
from flask_login import current_user
from .forms import AdminLoginForm

admin = Blueprint('admin', __name__)

@admin.route('/login')
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    form = AdminLoginForm()
    return render_template('admin/login.html', title='Login', form=form)


@admin.route('/logout')
def admin_logout():
    pass


@admin.route('/')
@admin.route('/dashboard')
def admin_dashboard():
    return render_template('admin/dashboard.html')
