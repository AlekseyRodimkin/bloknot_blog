from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5

# The structure in the form of a visual model in "../migrations/db_struct"
# The image corresponds to the migration version by name

# table of subscriber associations
followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                     )


class User(UserMixin, db.Model):
    """User model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')  # one to many to Post
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

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

    def avatar(self, size):
        """
        Avatar generation function.
        Default size = 80x80.
        :param size: size of the avatar (s=128 == 128x128)
        :return: link: str (maybe custom)
        """
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user):
        """Subscription function"""
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        """Unsubscribe function"""
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        """Subscription verification function"""
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        """
        The function of receiving posts from people of interest.

        .join() - a list of all the messages that a user is following
        .filter() - a subset of this list, messages that are followed by only one user
        .order_by() - sorting by time
        own - own posts
        :returns: combining posts subscriptions and personal, sorting by time
        """
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())


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
