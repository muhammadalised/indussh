from flask import Flask, render_template, redirect, url_for, Blueprint, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from .forms import AdminLoginForm, AddStaffForm, ProductForm
from indussh.models import Product, User, Order, Role
from indussh.admin.utils import save_picture

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
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin.login'))

@admin.route('/')
@admin.route('/dashboard')
@login_required
def dashboard():
    products_count = Product.query.count()
    staff_count = User.query.count()
    orders_count = Order.query.count()
    return render_template('admin/dashboard.html', 
                            products_count=products_count,
                            staff_count=staff_count,
                            orders_count=orders_count)

@admin.route('/staff')
@login_required
def display_staff():
    staff_users = User.query.all()
    return render_template('admin/staff.html', staff_users=staff_users)

@admin.route('/add-staff', methods=['GET', 'POST'])
@login_required
def add_staff():
    roles = Role.query.all()
    role_choices = [(r.id, r.name) for r in roles]
    role_choices.insert(0, (0, "Select a Role"))
    form = AddStaffForm()
    form.role.choices = role_choices

    if form.validate_on_submit():
        user = User(
            username = form.username.data,
            name = form.name.data,
            email = form.email.data,
            password = form.password.data,
        )
        if form.image_file.data:
            image_file = save_picture(form.image_file.data)
            user.image_file = image_file
        
        user.create()
        
        flash('Staff member added successfully!', 'success')
        return redirect(url_for('admin.add_staff'))
    return render_template('admin/staff-add.html', form=form)

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
    products = Product.query.all()
    # TODO: Complete the pagination
    return render_template('admin/products.html', products=products)

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
    orders = Order.query.all()
    return render_template('admin/orders.html', orders=orders)

@admin.route('/cancel-order/<int:order_id>')
@login_required
def cancel_order(order_id):
    pass