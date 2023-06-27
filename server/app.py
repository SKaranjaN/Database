from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, User, Comment


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


api = Api(app)

class Index(Resource):

    def get(self):
        response_dict = {
            "message" : "Database Home API"
        }
        response = make_response(
            response_dict,
            200
        )
        return response
api.add_resource(Index, "/")

class Users(Resource):

    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        response = make_response(
            jsonify(users),
            200
            )

        return response
    
    def post(self):
        new_user = User(
            name = request.form['name'],
        )
        db.session.add(new_user)
        db.session.commit()

        response_dict = new_user.to_dict()
        response = make_response(response_dict, 201)

        return response
api.add_resource(Users, "/users")

class User_by_Id(Resource):

    def get(self, id):
        response_dict = User.query.filter_by(id=id).first().to_dict()
        response = make_response(response_dict, 200)
        
        return response
    
    def patch(self, id):
        updated_one = User.query.filter_by(id=id).first()
        for attr in request.form:
            setattr(updated_one, attr, request.form[attr])

        db.session.add(updated_one)
        db.session.commit()

        response_dict = updated_one.to_dict()
        response = make_response(response_dict, 200)

        return response
    
    def delete(self, id):
        selected_one = User.query.filter_by(id=id).first()
        
        db.session.delete(selected_one)
        db.session.commit()

        response_dict = {"message": "Delete successfull"}
        response = make_response(
            jsonify(response_dict),
            200
        )
        return response

api.add_resource(User_by_Id, "/users/<int:id>")

class Comments(Resource):
    
    def get(self):
        comments = [comment.to_dict() for comment in Comment.query.all()]
        response = make_response(jsonify(comments), 200)

        return response
    
    def post(self):
        new_comment = Comment(
            post = request.form["post"],
        )
        db.session.add(new_comment)
        db.session.commit()

        response_dict = new_comment.to_dict()
        response = make_response(response_dict, 201)

        return response
api.add_resource(Comments, "/comments")

class Comment_By_Id(Resource):
    

    def get(self, id):
        comments = Comment.query.filter_by(id=id).first().to_dict()
        response = make_response(comments, 200)

        return response
api.add_resource(Comment_By_Id, "/comments/<int:id>")



if __name__ == '__main__':
    app.run(port=5555, debug=True)