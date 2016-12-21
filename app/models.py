# coding:utf8
from . import db
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from . import login_manager


class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    author = db.Column(db.Text)
    created = db.Column(db.DateTime, nullable=True)
    source = db.Column(db.Text)


class Art(db.Model):
    """
    作品
    """
    __tablename__ = 'art'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer)
    name = db.Column(db.Text)
    taobao_id = db.Column(db.Integer)
    image = db.Column(db.Text)


class Artist(db.Model):
    """
    艺术家
    """
    __tablename__ = 'artist'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.Text)
    location = db.Column(db.Text)
    introduction = db.Column(db.Text)
    image = db.Column(db.Text)
    pinyin = db.Column(db.Text)
    name = db.Column(db.Text)
    avatar = db.Column(db.Text)




class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))

    def verify_password(self, passwd):
        return check_password_hash(self.password, passwd)

    def get_id(self):
        try:
            return unicode(self.id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override get_id")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
