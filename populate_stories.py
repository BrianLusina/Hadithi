from app import db
from app.models import Story, Author

author = Author(full_name="", email="",password="")
story = Story(title="", tagline="", category="", content="", author_id=author.id)

db.session.add(author)
db.session.add(story)
db.session.commit()

