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
    # author = db.Column(db.Text)
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
    artist_id = db.Column(db.Integer)
    name = db.Column(db.Text)
    # taobao_id = db.Column(db.Integer)
    type = db.Column(db.Integer)
    art_list_image = db.Column(db.Text)
    art_enlarge_image = db.Column(db.Text)
    art_slide_image = db.Column(db.Text)
    subtitle = db.Column(db.Text)
    introduction = db.Column(db.Text)
    created = db.Column(db.DateTime)


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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
