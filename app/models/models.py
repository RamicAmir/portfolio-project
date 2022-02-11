"""
The module for User and Post.
Amer Ahmed
Amir Ramic
Supervisor: Joakim Wassberg
Version 0.0
"""

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from flask import current_app
from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    # Get user_id and return int
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """Modules User"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    profile = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(64), nullable=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def get_reset_token(self, expires_sec=1800):
        # Get reset token
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        # User verify token
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except ValueError:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.profile}')"


class Post(db.Model):
    """Modules Post"""
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    published = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.published}')"
