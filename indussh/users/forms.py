from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, HiddenField, IntegerField, SelectField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=60)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Sign Up')

class AdminForm(FlaskForm):
    name = StringField('Name', [Length(min=1, max=100)], render_kw={"placeholder":"Name"})
    email = StringField('Email', [Length(min=4, max=50)], render_kw={"placeholder":"Email"})
    password = PasswordField('Password', 
                            validators=[DataRequired()], 
                            render_kw={"placeholder":"Password"})
    confirm_password = PasswordField('Confirm Password', 
                            validators=[EqualTo('password', message='Passwords do not match')],
                            render_kw={"placeholder":"Confirm Password"})

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder":"Email"})
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

