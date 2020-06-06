from app import db, login

from hashlib import md5
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    authorised_items = db.relationship('Item', backref='author', lazy='dynamic')

    @classmethod
    def new_user(cls, username, email, password):
        u = cls()
        u.username = username
        u.email = email
        u.set_password(password)

        return u

    def __repr__(self):
        return f'<User: {self.username}>'

    def __eq__(self, other):
        return self.id == other.id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        mail_encode = md5(self.email.lower().encode('utf-8')).hexdigest()
        identicon_param = 'identicon'  # Tell gravatar to generate new random ones
        return f'https://www.gravatar.com/avatar/{mail_encode}?d={identicon_param}&s={size}'

    def add_item(self, item_title):
        item = Item.query.filter(Item.title == item_title).first()
        if item.author:
            raise Item.UnavailbleItem()

        self.authorised_items.append(item)

    def remove_item(self, item_title):
        item = Item.query.filter(Item.title == item_title).first()
        self.authorised_items.remove()

@login.user_loader
def load_user(user_id):
    """Method for helping flask login module loading users."""
    return User.query.get(int(user_id))


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    description = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Item {self.title}>'

    @classmethod
    def new_item(cls, title, description):
        item = cls()
        item.title = title
        item.description = description

        return item

    class UnavailbleItem(BaseException):
        pass
