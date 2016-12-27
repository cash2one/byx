# coding:utf8
from . import db
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from . import login_manager


class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.Integer)  # 所属分类
    news_list_image = db.Column(db.Text)  # 列表图片
    news_detail_image = db.Column(db.Text)  # 详情页图片
    title = db.Column(db.Text)  # 标题
    overview = db.Column(db.Text)  # 概述
    content = db.Column(db.Text)  # 内容
    source = db.Column(db.Text)  # 来源
    created = db.Column(db.DateTime)
    image_illustrate = db.Column(db.Text)  # 图片概述
    template_content = db.Column(db.Text)  # 模版内容


class Art(db.Model):
    """
    作品
    """
    __tablename__ = 'art'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer)  # 对应的艺术家id
    name = db.Column(db.Text)  # 作品名称
    type = db.Column(db.Integer)  # 作品类型
    art_list_image = db.Column(db.Text)  # 作品列表图片
    art_enlarge_image = db.Column(db.Text)  # 作品放大图片，用于作品详情页无"走进生活"图时的上部图，单张
    art_slide_image = db.Column(db.Text)  # 作品幻灯图片，用于"TA的其他作品"
    subtitle = db.Column(db.Text)
    introduction = db.Column(db.Text)
    created = db.Column(db.DateTime)

    index_slider_image = db.Column(db.Text)  # 首页轮播图片
    life_image = db.Column(db.Text)  # 走进生活图片，即详情页上部轮播
    index_life_image = db.Column(db.Text)  # 首页轮播图片对应的走进生活的图片，取的是走进生活第一张


class Artist(db.Model):
    """
    艺术家
    """
    __tablename__ = 'artist'
    id = db.Column(db.Integer, primary_key=True)
    # country = db.Column(db.Text)
    location = db.Column(db.Text)
    introduction = db.Column(db.Text)
    # image = db.Column(db.Text)
    pinyin = db.Column(db.Text)
    name = db.Column(db.Text)
    avatar = db.Column(db.Text)  # 艺术家头像
    slide_image = db.Column(db.Text)  # 艺术家幻灯片用图
    list_image = db.Column(db.Text)  # 艺术家列表用图
    created = db.Column(db.DateTime)


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))
    created = db.Column(db.DateTime)

    def verify_password(self, passwd):
        return check_password_hash(self.password, passwd)

    def get_id(self):
        try:
            return unicode(self.id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override get_id")


class SlidePic(db.Model):
    __tablename__ = "slidepic"
    id = db.Column(db.Integer, primary_key=True)
    slider = db.Column(db.String(128))
    slider_live = db.Column(db.String(128))
    created = db.Column(db.DateTime)


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer)
    son_id = db.Column(db.Integer)
    parent_name = db.Column(db.String(45))
    son_name = db.Column(db.String(45))


class Branch(db.Model):
    __tablename__ = 'branch'
    id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer)
    branch_name = db.Column(db.String(45))


class ArtType(db.Model):
    __tablename__ = 'art_type'
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer)
    type_name = db.Column(db.String(45))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
