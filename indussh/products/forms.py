from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import  Email, DataRequired, EqualTo, ValidationError, Length


class BillingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=60)])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    postcode = StringField('Zip/Post Code', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    notes = TextAreaField('Order Notes')
    
    submit = SubmitField('Place Order')