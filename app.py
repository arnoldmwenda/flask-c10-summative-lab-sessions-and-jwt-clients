from flask import Flask, request, session, jsonify
from flask_restful import Api, Resource
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from marshmallow import ValidationError

from config import Config
from models.db import db
from models.user import User
from models.note import Note
from models.schemas import user_schema, note_schema, notes_schema

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
api = Api(app)


def current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return User.query.get(user_id)


class Signup(Resource):
    def post(self):
        json_data = request.get_json() or {}

        try:
            data = user_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        existing_user = User.query.filter_by(username=data["username"]).first()
        if existing_user:
            return {"error": "Username already taken"}, 422

        new_user = User(username=data["username"])
        new_user.password = data["password"]

        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.id

        return user_schema.dump(new_user), 201


class Login(Resource):
    def post(self):
        json_data = request.get_json() or {}
        username = json_data.get("username")
        password = json_data.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.authenticate(password):
            session["user_id"] = user.id
            return user_schema.dump(user), 200

        return {"error": "Invalid username or password"}, 401


class Logout(Resource):
    def delete(self):
        if not session.get("user_id"):
            return {"error": "Not logged in"}, 401

        session["user_id"] = None
        return {}, 204


class CheckSession(Resource):
    def get(self):
        user = current_user()
        if user:
            return user_schema.dump(user), 200
        return {"error": "Not logged in"}, 401





api.add_resource(Signup, "/signup")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(CheckSession, "/check_session")




if __name__ == "__main__":
    app.run(port=5555, debug=True)
