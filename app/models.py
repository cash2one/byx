from . import db


class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    author = db.Column(db.Text)
    created = db.Column(db.DateTime, nullable=True)
    source = db.Column(db.Text)


class Art(db.Model):
    __tablename__ = 'art'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer)
    name = db.Column(db.Text)
    taobao_id = db.Column(db.Integer)
    image = db.Column(db.Text)


class Artist(db.Model):
    __tablename__ = 'artist'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.Text)
    location = db.Column(db.Text)
    introduction = db.Column(db.Text)
    image = db.Column(db.Text)