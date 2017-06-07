"""
Forms that will be used in entire application
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from app.mod_auth.models import AuthorAccount


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
    who has logged in.
    Checks if the entered email, i.e. if the email is altered is already in use in the db and warns the user
    does the same for user names
    :cvar first_name :user can be able to change their first name with this field
    :cvar last_name :user can change their last name withi this field
    :cvar username :user name as per the current user from the db
    :cvar email :current user's email, user can change their email address
    :cvar about_me :text area field where the user will enter text about themselves
    :cvar edit_profile :submit button to save details about the new profile
    """
    first_name = StringField()
    last_name = StringField()
    username = StringField()
    about_me = TextAreaField(validators=[Length(max=250, message="Maximum characters exceeded")])
    edit_profile = SubmitField("Update Profile")

    def __init__(self, new_username, *args, **kwargs):
        """
        creates a new EditForm object
        """
        super().__init__(*args, **kwargs)
        self.new_username = new_username

    def validate_form(self):
        """
        Validates the edit profile form before submission
        This will check the database for any similar usernames and if there is already a username in use
        inform the user and display an error
        :return: True if the credentials are ok, false otherwise
        :rtype: bool
        """
        initial_validation = super(EditProfileForm, self).validate()
        if not initial_validation:
            return False
        if self.username.data == self.new_username:
            return True

        author = AuthorAccount.query.filter_by(username=self.username.data).first()

        # if author already exists return false
        if author is not None:
            self.username.errors.append("This username is already in use, please pick another")
            return False

        # else, all is well, return true
        return True
