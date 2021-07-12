from flask import Flask, render_template, session, redirect, url_for, Blueprint
from indussh.admin.forms import AdminForm
from indussh.models import User

admin = Blueprint('Admin', __name__)


@admin.route('/admin/login')
def admin_login():
    pass


@admin.route('/admin/logout')
def admin_logout():
    pass


@admin.route('/admin')
@admin.route('/admin/dashboard')
def admin_dashboard():
    pass
