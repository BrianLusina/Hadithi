from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from app.models import Author


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
    :cvar full_name: Full name of registering author
    :cvar username: username to identify author
    :cvar email: email Author will use to register account
    :cvar password: password the Author will use to login/ perform tasks
    """
    full_name = StringField(validators=[DataRequired()])
    username = StringField(validators=[DataRequired(), Length(min=5, max=15)])
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired(),
                                         EqualTo('verify_password', message="Passwords must match"),
                                         Length(min=8, max=15)
                                         ])
    verify_password = PasswordField(validators=[DataRequired()])
    register = SubmitField("REGISTER")

    def validate_form(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = Author.query.filter_by(email=self.email.data).first()
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


class StoryForm(FlaskForm):
    """
    Story form is used to write the actual story to be shared with others
    :cvar story_title: Title of the Author
    :cvar tagline: Tageline for this story
    :cvar content: The actual content for the story
    """
    story_title = StringField(validators=[DataRequired()])
    tagline = StringField(validators=[DataRequired(), Length(min=1, max=50)])
    category = StringField(validators=[DataRequired()])
    content = TextAreaField(validators=[DataRequired()])
    save = SubmitField("SAVE")


class ContactForm(FlaskForm):
    """
    Contact form for site used to submit contact details to server
    """
    sender_name = StringField(validators=[DataRequired()])
    sender_email = StringField(validators=[DataRequired(), Email()])
    sender_message = TextAreaField(validators=[DataRequired()])
    send_message = SubmitField("Send Message")
