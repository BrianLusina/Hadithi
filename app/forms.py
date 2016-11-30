from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(Form):
    email = StringField(label="Email/username", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])


class RegisterForm(Form):
    first_name = StringField(label="First Name", validators=[DataRequired()])
    second_name = StringField(label="Last Name", validators=[DataRequired()])
    username = StringField(label="Username", validators=[DataRequired(), Length(min=5, max=15)])
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password",
                             validators=[DataRequired(),
                                         EqualTo('verify_password', message="Passwords must match"),
                                         Length(min=8, max=15)
                                         ])
    verify_password = PasswordField(label="Retype Password", validators=[DataRequired()])
