from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Regexp, EqualTo
from shop.models import User

class RegistrationForm(FlaskForm):
    username_new = StringField('Username',validators=[DataRequired(), Regexp('^[A-Za-z0-9]{5,20}$', message='Your username should be between 5 and 20 characters long, and can only contain letters and numbers.')])
    password_new = PasswordField('Password',validators=[DataRequired(), Regexp('^[A-Za-z0-9]{5,20}$', message='Your password should be between 5 and 20 characters long, and can only contain letters and numbers.')])
    password_confirm = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password_new', message='Passwords do not match. Please try again.')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exists. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')

class CheckoutForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    card_no = StringField('Card Number', validators=[DataRequired(), Regexp('[0-9]{16}', message='Your card number must be 16 digits long.')])
    submit = SubmitField('Submit')

class SortForm(FlaskForm):
    sort_type = SelectField("Sort by", choices=[("price_high", "High Price"), ("price_low", "Low Price"), ("eco_low", "Low Eco")], default="price_high", render_kw={"onchange": "this.form.submit()"})