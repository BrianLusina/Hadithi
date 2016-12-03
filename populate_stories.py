from app import db
from app.models import Story, Author
import json

stories = open("stories.json", "r")
authors = open("authors.json", "r")

with stories as data:
    loaded_stories = json.load(data)

with authors as data:
    loaded_authors = json.load(data)

for l_story in loaded_stories:
    for auth in loaded_authors:
        author = Author(full_name=auth["full_name"], email=auth["email"], password=auth["password"])
        story = Story(title=l_story.get("title"), tagline=l_story.get("tagline"),
                      category=l_story.get("category"), content=l_story.get("content"), author_id=author.id)
        db.session.add(author)
        db.session.add(story)
db.session.commit()



