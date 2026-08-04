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





if __name__ == "__main__":
    app.run(port=5555, debug=True)
