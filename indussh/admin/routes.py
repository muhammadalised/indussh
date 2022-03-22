from flask import Flask, render_template, session, redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from indussh import db
from indussh.models import User, Product

admin = Admin(name='Indussh-Admin', template_mode='bootstrap3')

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Product, db.session))

# @admin.route('/admin/login')
# def admin_login():
#     if current_user.is_authenticated:
#         return redirect(url_for('admin_dashboard'))
#     form = LoginForm()
#     return render_template('admin/login.html', title='Login', form=form)


# @admin.route('/admin/logout')
# def admin_logout():
#     pass


# @admin.route('/admin')
# @admin.route('/admin/dashboard')
# def admin_dashboard():
#     pass
