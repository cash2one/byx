#!/usr/bin/env python
# coding:utf8

from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField, RadioField
from wtforms.validators import DataRequired, EqualTo
from ..models import Artist


class LoginForm(Form):
    username = StringField(u'Username', validators=[DataRequired()])
    password = PasswordField(u'Password', validators=[DataRequired()])
    submit = SubmitField(u'Login')


class RegisterForm(Form):
    username = StringField(u'Username', validators=[DataRequired()])
    password = PasswordField(u'Password', validators=[DataRequired(), EqualTo('password_confirm', message=u'两次密码不匹配')])
    password_confirm = PasswordField(u'密码(确认)')
    submit = SubmitField()


class ChangePasswordForm(Form):
    current_password = PasswordField(u'当前密码', validators=[DataRequired()])
    new_password = PasswordField(u'新密码',
                                 validators=[DataRequired(), EqualTo('new_password_confirm', message=u'两次密码不匹配')])
    new_password_confirm = PasswordField(u'新密码(确认)', validators=[DataRequired()])
    submit = SubmitField(u'保存改动')


class SlidePicForm(Form):
    slider = FileField(u'轮播图片', validators=[DataRequired()])
    slider_live = FileField(u'走进生活图片', validators=[DataRequired()])
    submit = SubmitField(u'点击保存')


class ArtistForm(Form):
    location = StringField(u'籍贯', validators=[DataRequired()])
    pinyin = StringField(u'拼音', validators=[DataRequired()])
    name = StringField(u'姓名', validators=[DataRequired()])
    avatar = FileField(u'头像', validators=[DataRequired()])
    list_image = FileField(u'艺术家幻灯片用图', validators=[DataRequired()])
    slide_image = FileField(u'艺术家列表用图', validators=[DataRequired()])
    introduction = TextAreaField(u'简介', validators=[DataRequired()])
    submit = SubmitField(u'点击保存')


class ArtForm(Form):
    artist_id = SelectField(u'艺术家', coerce=int, validators=[DataRequired()])
    type = RadioField(u'作品类型', coerce=int, validators=[DataRequired()])
    art_list_image = FileField(u'作品列表图片', validators=[DataRequired()])
    art_enlarge_image = FileField(u'作品放大图片', validators=[DataRequired()])
    art_slide_image = FileField(u'作品幻灯图片', validators=[DataRequired()])
    name = StringField(u'名称', validators=[DataRequired()])
    subtitle = StringField(u'副标题', validators=[DataRequired()])
    introdution = TextAreaField(u'简介', validators=[DataRequired()])
    submit = SubmitField(u'点击保存')

    def __init__(self, *args, **kwargs):
        super(ArtForm, self).__init__(*args, **kwargs)
        self.artist_id.choices = [(i.id, i.name) for i in Artist.query.all()]
        self.type.choices = [(0, u'珂罗版'), (1, u'丝网版'), (2, u'木版'), (3, u'铜版'), (4, u'石版'), (5, u'综合版'),
                             (6, u'艺术微喷'), (7, u'艺术衍生品'), (8, u'艺术走进生活'), (99, u'其他')]


class NewsForm(Form):
    category = SelectField(u'所属分类', coerce=int, validators=[DataRequired()])
    news_list_image = FileField(u'动态列表图片', validators=[DataRequired()])
    news_detail_image = FileField(u'动态列表图片', validators=[DataRequired()])
    title = StringField(u'标题', validators=[DataRequired()])
    source = StringField(u'来源', validators=[DataRequired()])
    overview = TextAreaField(u'概述', validators=[DataRequired()])
    image_illustrate = StringField(u'图片说明', validators=[DataRequired()])
    content = TextAreaField(u'详细内容', validators=[DataRequired()])
    template_content = TextAreaField(u'模版内容', validators=[DataRequired()])
    submit = SubmitField(u'点击保存')

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        self.category.choices = [(0, u'动态-百雅轩动态'), (1, u'动态-艺术家资讯'), (2, u'动态-其他'),
                                 (3, u'活动-展览资讯'), (4, u'活动-相关活动'), (5, u'活动-其他'),
                                 (6, u'关于我们-版画制作工艺'), (7, u'关于我们-艺术家与百雅轩')]
