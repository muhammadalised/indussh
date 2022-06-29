from flask import Flask, render_template, redirect, url_for, Blueprint, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from .forms import AdminLoginForm, StaffForm, ProductForm
from indussh.models import User

admin = Blueprint('admin', __name__)

@admin.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    form = AdminLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin.dashboard'))
        
        flash('Invalid email or password.', 'danger')
    return render_template('admin/login.html', title='Login', form=form)

@admin.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('admin.login'))

@admin.route('/')
@admin.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/dashboard.html')

@admin.route('/staff')
@login_required
def display_staff():
    return render_template('admin/staff.html')

@admin.route('/add-staff')
@login_required
def add_staff():
    return render_template('admin/staff-add.html')

@admin.route('/delete-staff/<int:id>')
@login_required
def delete_staff(id):
    pass

@admin.route('/edit-staff/<int:id>')
@login_required
def edit_staff(id):
    pass

@admin.route('/customers')
@login_required
def display_customers():
    return render_template('admin/customers.html')

@admin.route('/products')
@login_required
def display_products():
    return render_template('admin/products.html')

@admin.route('/add-product')
@login_required
def add_product():
    return render_template('admin/products-add.html')

@admin.route('/delete-product/<int:product_id>')
@login_required
def delete_product(product_id):
    pass

@admin.route('/edit-product/<int:product_id>')
@login_required
def edit_product(product_id):
    pass

@admin.route('/orders')
@login_required
def orders():
    return render_template('admin/orders.html')

@admin.route('/cancel-order/<int:order_id>')
@login_required
def cancel_order(order_id):
    pass