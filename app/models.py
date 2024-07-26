from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


class User(UserMixin, db.Model):
    """User model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')  # one to many to Post

    def __repr__(self):
        """
        The function returns an unambiguous representation of the users as a string
        :return: str
        """
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        """
        Password replacement function
        :param password: user password
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Password verification function
        :param password: user password
        :return: boolean
        """
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    """Post model"""
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # many to one to Users

    def __repr__(self):
        """
        The function returns an unambiguous representation of the posts as a string
        :return: str
        """
        return '<Post {}>'.format(self.body)


@login.user_loader
def load_user(id):
    """
    The function will configure the user loader function,
    which can be called to load a user with an ID
    :param id: user ID
    """
    return User.query.get(int(id))
