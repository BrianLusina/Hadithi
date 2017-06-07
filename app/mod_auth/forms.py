from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from .models import AuthorAccount


class LoginForm(FlaskForm):
    """
    Login form for authors to access Hadithi
    :cvar email: email of the Author logging int
    :cvar password: Password for the Author to login
    :cvar login: Login button to submit form data
    :cvar remember_me: checkbox to keep user session alive for as long as they are logged in.
    """
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    login = SubmitField("LOG IN")
    remember_me = BooleanField()


class RegisterForm(FlaskForm):
    """
    Register form for authors to register with the site
    :cvar first_name: First name of registering author
    :cvar last_name: last name/surname of user
    :cvar username: username to identify author
    :cvar email: email Author will use to register account
    :cvar password: password the Author will use to login/ perform tasks
    """
    first_name = StringField(validators=[DataRequired()])
    last_name = StringField(validators=[DataRequired()])
    username = StringField(validators=[DataRequired(), Length(min=5, max=15)])
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired(),
                                         EqualTo('verify_password', message="Passwords must match"),
                                         Length(min=8, max=15)
                                         ])
    verify_password = PasswordField(validators=[DataRequired()])
    register = SubmitField("REGISTER")

    def validate_form(self):
        """
        pre-validation of register form. This will check the db if there is a user with the email
        and warn the user that this email already exists.
        :return: True if the user email already exists, False otherwise
        :rtype: bool
        """
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = AuthorAccount.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True


class ForgotPassword(FlaskForm):
    """
    Password recovery form
    :cvar email: Email of the user
    :cvar send_mail: Submit button for form data
    """
    email = StringField(validators=[DataRequired(), Email()])
    send_mail = SubmitField("SEND EMAIL")
