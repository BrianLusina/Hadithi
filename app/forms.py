from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    login = SubmitField("LOG IN")
    remember_me = BooleanField()


class RegisterForm(FlaskForm):
    full_name = StringField(validators=[DataRequired()])
    username = StringField(validators=[DataRequired(), Length(min=5, max=15)])
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired(),
                                         EqualTo('verify_password', message="Passwords must match"),
                                         Length(min=8, max=15)
                                         ])
    verify_password = PasswordField(validators=[DataRequired()])
    register = SubmitField("REGISTER")


class ForgotPassword(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    send_mail = SubmitField("SEND EMAIL")