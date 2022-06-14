from flask import Flask, render_template, redirect, url_for, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from .forms import AdminLoginForm
from indussh.models import User

admin = Blueprint('admin', __name__)

@admin.route('/login')
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    form = AdminLoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        

    return render_template('admin/login.html', title='Login', form=form)

@admin.route('/logout')
def admin_logout():
    pass


@admin.route('/')
@admin.route('/dashboard')
def admin_dashboard():
    return render_template('admin/dashboard.html')

@admin.route('/staff')
def display_staff():
    pass

@admin.route('/add-staff')
def add_staff():
    pass

@admin.route('/delete-staff/<int:id>')
def delete_staff(id):
    pass

@admin.route('/edit-staff/<int:id>')
def edit_staff(id):
    pass

@admin.route('/products')
def display_products():
    pass

@admin.route('/add-product')
def add_product():
    pass

@admin.route('/delete-product/<int:product_id>')
def delete_product(product_id):
    pass

@admin.route('/edit-product/<int:product_id>')
def edit_product(product_id):
    pass

@admin.route('/orders')
def orders():
    pass

@admin.route('/cancel-order/<int:order_id>')
def cancel_order(order_id):
    pass