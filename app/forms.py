"""
Forms that will be used in entire application
"""
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from app.models import AuthorAccount


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
    publish = SubmitField("PUBLISH")
    save_draft = SubmitField("SAVE DRAFT")


class ContactForm(FlaskForm):
    """
    Contact form for site used to submit contact details to server
    """
    sender_name = StringField(validators=[DataRequired()])
    sender_email = StringField(validators=[DataRequired(), Email()])
    sender_message = TextAreaField(validators=[DataRequired()])
    send_message = SubmitField("Send Message")


class EditProfileForm(FlaskForm):
    """
    Form for users to be able to edit the profile accounts
    Allow users to edit their username, email, first and last names, about me section and password
    These fields should have defaults that will be populated from the database based on the current user
    who has logged in
    :cvar first_name :user can be able to change their first name with this field
    :cvar last_name :user can change their last name withi this field
    :cvar user_name :user name as per the current user from the db
    :cvar email :current user's email, user can change their email address
    :cvar about_me :text area field where the user will enter text about themselves
    :cvar edit_profile :submit button to save details about the new profile
    """
    first_name = StringField(default=current_user.first_name)
    last_name = StringField(default=current_user.last_name)
    user_name = StringField(default=current_user.username)
    email = StringField(default=current_user.email, validators=[Email()])
    about_me = TextAreaField(validators=[Length(min=0, max=250)])
    edit_profile = SubmitField("Update Profile")
