"""
Forms that will be used in entire application
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


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
