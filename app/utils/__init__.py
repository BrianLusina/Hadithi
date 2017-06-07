from app import db
from app.mod_auth.models import AuthorAccount
from app.mod_story.models import Story
import json
from datetime import datetime


class InitDatabase(object):
    """
    Initializes the database with default records
    """
    def __init__(self):
        pass

    def add_stories(self):
        """
        Adds stories to the database
        :return:
        """
        authors = open("app/utils/authors.json", "r")
        stories = open("app/utils/stories.json", "r")

        with stories as story_data:
            loaded_stories = json.load(story_data)

        with authors as author_data:
            loaded_authors = json.load(author_data)

        author_story = list(zip(loaded_authors, loaded_stories))

        for au_st in author_story:
            author = AuthorAccount(first_name=au_st[0]["first_name"], last_name=au_st[0]["last_name"],
                                   email=au_st[0]["email"], username=au_st[0]["username"],
                                   password=au_st[0]["password"], registered_on=datetime.now())
            
            story = Story(title=au_st[1]["title"], tagline=au_st[1]["tagline"],
                          category=au_st[1]["category"], content=au_st[1]["content"], author_id=author.id)
            db.session.add(author)
            db.session.add(story)
        db.session.commit()
