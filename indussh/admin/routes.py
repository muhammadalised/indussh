from flask import Flask, render_template, session, redirect, url_for, Blueprint
from indussh.admin.forms import AdminForm
from indussh.users.forms import LoginForm
from indussh.models import User
from flask_login import login_user, logout_user, current_user, login_required

admin = Blueprint('Admin', __name__)


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
