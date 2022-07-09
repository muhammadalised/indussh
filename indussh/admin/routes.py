from flask import render_template, redirect, url_for, Blueprint, flash, request, current_app
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import func

from .forms import AdminCreateForm, AdminLoginForm, ProductAddForm, AdminUpdateForm
from indussh.models import db, Product, Customer, User, Order, Role
from indussh.admin.utils import save_picture, clean_text

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/')
@admin.route('/dashboard')
@login_required
def dashboard():
    product_count = Product.query.count()
    customer_count = Customer.query.count()
    order_count = Order.query.count()
    total_sales = Order.query.with_entities(func.sum(Order.amount).label('total_sales')).filter(Order.completed==True).first().total_sales
    avg_order_sale = int(Order.query.with_entities(func.avg(Order.amount).label('avg_order_sale')).filter(Order.completed==True).first().avg_order_sale)
    return render_template('admin/dashboard.html', 
                            product_count=product_count,
                            customer_count=customer_count,
                            order_count=order_count,
                            total_sales=total_sales,
                            avg_order_sale=avg_order_sale)

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

@admin.route('/admins')
@login_required
def display_admins():
    admins = User.query.all()
    return render_template('admin/admins.html', admins=admins)

@admin.route('/profile', methods=['GET', 'POST'])
@login_required
def admin_profile():
     # TODO: Add functionality to update password as well
    form = AdminUpdateForm()
    if form.validate_on_submit():
        if form.image_file.data:
            image_file = save_picture(form.image_file.data, 
                                        current_app.config['PROFILE_IMAGES_PATH'],
                                        current_app.config['PROFILE_IMAGE_SIZE'])
            current_user.image_file = image_file
        
        current_user.name = form.name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('admin.admin_profile'))
    elif request.method == 'GET':
         # Populate the form fields with data from the database
        form.name.data = current_user.name
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('admin/admin-profile.html', form=form)

@admin.route('/add', methods=['GET', 'POST'])
@login_required
def add_admin():
    roles = Role.query.filter(Role.name != 'Customer').all()
    role_choices = [(r.id, r.name) for r in roles]
    role_choices.insert(0, (0, "Select a Role"))
    form = AdminCreateForm()
    form.role.choices = role_choices

    if form.validate_on_submit():
        
        user = User(
            username = form.username.data,
            name = form.name.data,
            email = form.email.data,
            password = form.password.data,
            role_id = form.role.data
        )
        if form.image_file.data:
            image_file = save_picture(form.image_file.data, 
                                        current_app.config['PROFILE_IMAGES_PATH'],
                                        current_app.config['PROFILE_IMAGE_SIZE'])
            user.image_file = image_file
        
        user.create()
        
        flash('Staff member added successfully!', 'success')
        return redirect(url_for('admin.add_admin'))
    return render_template('admin/admin-add.html', form=form)

@admin.route('/<int:admin_id>/delete', methods=['POST'])
@login_required
def delete_admin(admin_id):
    staff = User.query.get_or_404(admin_id)
    db.session.delete(staff)
    db.session.commit()
    flash('Admin record deleted successfully', 'success')
    return redirect(url_for('admin.display_admins'))

@admin.route('/customers')
@login_required
def display_customers():
    customers = Customer.query.all()
    return render_template('admin/customers.html', customers=customers)

@admin.route('/products')
@login_required
def display_products():
    products = Product.query.order_by(Product.added_on.desc()).all()
    return render_template('admin/products.html', products=products)

@admin.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductAddForm()
    if form.validate_on_submit():
        product = Product(
            article_no=form.article.data, name=form.name.data,
            description=clean_text(form.description.data), type=form.type.data, 
            category=form.category.data, price=form.price.data, 
            minimum_price=form.min_price.data,
            size_sm=form.size_s.data, size_md=form.size_m.data,
            size_l=form.size_l.data, size_xl=form.size_xl.data
        )
        
        if form.image_file.data:
            image_file = save_picture(form.image_file.data, 
                                        current_app.config['PRODUCT_IMAGES_PATH'],
                                        current_app.config['PRODUCT_IMAGE_SIZE'])
            product.image_file = image_file
        
        product.create()
        flash('Product Added Successfully', 'success')
        return redirect(url_for('admin.add_product'))

    return render_template('admin/products-add.html', form=form)

@admin.route('/<int:product_id>/delete-product', methods=['GET', 'POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted', 'success')
    return redirect(url_for('admin.display_products'))

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

# General flow for placing orders in context of models
# 1. The customer data is stored first in db
# 2. Order object is initialized and added
# 3. Order Item object is initialized and added
# 4. commit the changes