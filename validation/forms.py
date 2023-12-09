# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField,BooleanField
from wtforms.validators import DataRequired, Email, Length, Regexp, NumberRange, EqualTo, InputRequired


class RegistrationForm(FlaskForm):
    username_give = StringField('username', validators=[
        DataRequired(),
        Length(min=3, max=10, message='Username must be between 3 and 10 characters'),
        Regexp('^[A-Z][A-Za-z0-9]*$',
               message='Username must start with a capital letter and contain only letters and numbers'),
    ])
    fullname_give = StringField('fullname', validators=[
        DataRequired(),
        Length(min=4, max=20, message='Fullname must be between 3 and 10 characters'),
        Regexp(
            '^[A-Z]', message='Fullname must start with a capital letter and contain only letters and numbers')
    ])
    email_give = StringField('email', validators=[DataRequired(), Email()])
    password_give = PasswordField('password', validators=[
        DataRequired(),
        Length(min=3, max=10, message='Password must be between 3 and 10 characters'),
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password_give')])
    submit = SubmitField('register')


class LoginForm(FlaskForm):
    username_give = StringField('username', validators=[DataRequired()])
    password_give = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('login')


class DonateForm(FlaskForm):
    country_give = StringField('Country', validators=[DataRequired(
        message='Country is required')])  # Should be a string
    donate_give = IntegerField('Donation', validators=[DataRequired(message='Donation amount is required'), NumberRange(
        min=0, message='Donation amount should be a positive number')])  # Should be a number for currency
    email_give = StringField('Email', validators=[
                             DataRequired(), Email()])  # Should be an email
    agree_give = BooleanField('Agree',  default=True)  # Should be a boolean
    phone_give = StringField('Phone', validators=[DataRequired(), Length(min=10, message='Should be a phone with a minimum length of 10digit'), Regexp(
        '^[0-9]+$', message='Must be a string for phone number')])  # Should be a string for phone number
    rekening_give = StringField('Rekening', validators=[
        DataRequired(message='Bank account is required'),
        Length(min=10, message='Bank account should be at least 10 digits'),
        Regexp('^[0-9]+$', message='Bank account must be a string or number')
    ])
    expiry_date_give = StringField('Expiry Date', validators=[
        DataRequired(message='Expiry date is required'),
        Regexp('^(0[1-9]|1[0-2])\/(1[2-9]|2[0-9])$',
               message='Should be a string in MM/YY format')
    ])
    security_code_give = IntegerField('Security Code', validators=[
        DataRequired(message='Security code is required'),
        NumberRange(min=3, message='Must be a number with at least 3 digits')
    ])
    fullname_give = StringField('Fullname', validators=[
        DataRequired(message='Fullname is required'),
        Length(min=3, message='Should be a string with a minimum length of 3')
    ])
    submit = SubmitField('donate')
