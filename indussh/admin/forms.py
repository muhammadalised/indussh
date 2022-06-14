from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError


class AdminForm(FlaskForm):
    name = StringField('Name', [Length(min=1, max=100)], render_kw={"placeholder": "Name"})
    email = StringField('Email', [Length(min=4, max=50), Email(), DataRequired()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password',
                                     validators=[
                                         EqualTo('password', message='Passwords do not match')],
                                     render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Create Admin')

class AdminLoginForm(FlaskForm):
    email = StringField('Email', [Length(min=4, max=50), Email(), DataRequired()], render_kw={
                        "placeholder": "Email"})
    password = PasswordField('Password',
                             validators=[DataRequired()],
                             render_kw={"placeholder": "Password"})

class ProductForm(FlaskForm):
    article = StringField('Product Article No', [
        Length(min=1, max=100),
        DataRequired()],
        render_kw={"placeholder": "Article No"})
    name = StringField('Product Name', [
        Length(min=1, max=100),
        DataRequired()
    ], render_kw={"placeholder": "Name"})
    type = StringField('Product Category', [
        Length(min=1, max=100),
        DataRequired()
    ], render_kw={"placeholder": "Product Category"})
    category = StringField('Product Type', [
        Length(min=1, max=100),
        DataRequired()
    ], render_kw={"placeholder": "Product Type"})

    description = TextAreaField('Product Description', [DataRequired()], render_kw={
                                "placeholder": "Description"})
    price = IntegerField('Product Price', [
        DataRequired()], render_kw={"placeholder": "Price"})
    min_price = IntegerField('Product Minimum Acceptable Price', [
        DataRequired()], render_kw={"placeholder": "Minimum Acceptable Price"})

    image_file = FileField('Add Product Picture', validators=[
                           FileAllowed(['jpg', 'png'])])

    size_s = IntegerField('Size Small', render_kw={
                          "placeholder": "Enter Quantity for Small", "value": 0})
    size_m = IntegerField('Size Medium', render_kw={
                          "placeholder": "Enter Quantity for Medium", "value": 0})
    size_l = IntegerField('Size Large', render_kw={
                          "placeholder": "Enter Quantity for Large", "value": 0})
    size_xl = IntegerField('Size Extra Large', render_kw={
                           "placeholder": "Enter Quantity for Extra Large", "value": 0})

    submit = SubmitField('Add Product')
