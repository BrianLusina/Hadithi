from app import db
from app.models import Story, Author
import json

stories = open("stories2.json", "r")
with stories as data:
    loaded_stories = json.load(data)

author = Author(full_name="Brian M", email="brianombito@email.com", password="password")
db.session.add(author)

for l_story in loaded_stories:
    story = Story(title=l_story.get("title"), tagline=l_story.get("tagline"),
                  category=l_story.get("category"), content=l_story.get("content"), author_id=author.id)

    db.session.add(story)
db.session.commit()
