from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    serialize_rules = ("-comments.user")
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())

    comments = db.relationship("Comment", backref = "user")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }
    

    def __repr__(self):
        return f'<User: {self.name}>'



class Comment(db.Model, SerializerMixin):
    __tablename__ = "comments"

    serialize_rules = ("-user.comments")
    id = db.Column(db.Integer(), primary_key=True)
    post = db.Column(db.String())
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    
    

    def __repr__(self):
        return f'<Comment: {self.post}>'
