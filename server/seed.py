from faker import Faker

from app import app
from models import db, User, Comment

with app.app_context():
    
    fake = Faker()

    User.query.delete()

    users = []
    for i in range(50):
        user = User(
            name=fake.name()
        )
        users.append(user)

    db.session.add_all(users)
    db.session.commit()

    Comment.query.delete()

    comments = []
    for i in range(50):
        comment = Comment(
            post = fake.paragraph(nb_sentences=5)
        )
        comments.append(comment)

    db.session.add_all(comments)
    db.session.commit()