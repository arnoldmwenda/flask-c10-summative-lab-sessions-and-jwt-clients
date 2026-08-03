from sqlalchemy.ext.hybrid import hybrid_property
from flask_bcrypt import Bcrypt

from models.db import db

bcrypt = Bcrypt()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    _password_hash = db.Column(db.String(128), nullable=False)

    notes = db.relationship(
        "Note",
        backref="user",
        cascade="all, delete-orphan"
    )

    @hybrid_property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, plain_text_password):
        password_hash = bcrypt.generate_password_hash(
            plain_text_password.encode("utf-8")
        )
        self._password_hash = password_hash.decode("utf-8")

    def authenticate(self, plain_text_password):
        return bcrypt.check_password_hash(
            self._password_hash, plain_text_password
        )

    def __repr__(self):
        return f"<User id={self.id} username={self.username}>"
