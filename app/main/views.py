# coding:utf8
from . import main
from flask import render_template, request, redirect, url_for, flash, current_app
from ..models import News, User, Artist, Art
from flask_login import current_user, login_user, login_required, logout_user
from .forms import LoginForm, RegisterForm, ChangePasswordForm, SlidePicForm, ArtistForm, ArtForm
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from .. import db
import os


# todo
# http://stackoverflow.com/questions/18600031/changing-the-active-class-of-a-link-with-the-twitter-bootstrap-css-in-python-fla
# 图片格式判断


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/about.html')
def about():
    return render_template('about_1.html')


@main.route('/about_tech.html')
def about_tech():
    return render_template('about_2.html')


@main.route('/artist.html')
def artist():
    return render_template('artistlist.html')


@main.route('/artistlive.html')
def artistlive():
    return render_template('artistlive.html')


@main.route('/artlive.html')
def artlive():
    return render_template('artlive.html')


@main.route('/artshow.html')
def artshow():
    return render_template('artshow.html')


@main.route('/exhibition.html')
def exhibition():
    id = request.args.get('id', '')
    if id:
        news = News.query.filter_by(id=id).first()
        return render_template('exhibition.html', news=news)
    else:
        print 'liebiao'


@main.route('/update.html', methods=['GET', 'POST'])
@login_required
def update():
    return render_template('update.html')


@main.route('/sliderpic.html', methods=['GET', 'POST'])
@login_required
def sliderpic():
    form = SlidePicForm()
    if form.validate_on_submit():
        filename1 = secure_filename(form.slider.data.filename)
        filename2 = secure_filename(form.slider_live.data.filename)
        file_path1 = os.path.join(current_app.config['UPLOAD_FOLDER'], filename1)
        file_path2 = os.path.join(current_app.config['UPLOAD_FOLDER'], filename2)
        form.slider.data.save(file_path1)
        form.slider_live.data.save(file_path2)
        return redirect(url_for("main.sliderpic"))
        # pass
    else:
        flash_errors(form)
    return render_template('sliderpic.html', form=form)


@main.route('/artistupdate.html', methods=['GET', 'POST'])
@login_required
def artistupdate():
    form = ArtistForm()
    if form.validate_on_submit():
        # todo
        # 如何保存图片路径

        location = form.location.data
        name = form.name.data
        introduction = form.introduction.data
        pinyin = form.pinyin.data
        filename1 = secure_filename(form.avatar.data.filename)
        filename2 = secure_filename(form.slide_image.data.filename)
        filename3 = secure_filename(form.list_image.data.filename)

        file_path1 = os.path.join(current_app.config['UPLOAD_FOLDER'], filename1)
        file_path2 = os.path.join(current_app.config['UPLOAD_FOLDER'], filename2)
        file_path3 = os.path.join(current_app.config['UPLOAD_FOLDER'], filename3)

        form.avatar.data.save(file_path1)
        form.slide_image.data.save(file_path2)
        form.list_image.data.save(file_path3)

        artist = Artist(location=location, name=name, pinyin=pinyin,
                        avatar=filename1, introduction=introduction,
                        slide_image=filename2,
                        list_image=filename3)
        db.session.add(artist)
        db.session.commit()
        return redirect(url_for("main.artistupdate"))

    else:
        flash_errors(form)
    return render_template('artistupdate.html', form=form)


@main.route('/artupdate.html', methods=["GET", "POST"])
@login_required
def artupdate():
    form = ArtForm()
    if form.validate_on_submit():

        name = form.name.data
        iintroduction = form.introdution.data
        subtitle = form.subtitle.data

        filename1 = secure_filename(form.art_list_image.data.filename)
        filename2 = secure_filename(form.art_enlarge_image.data.filename)
        filename3 = secure_filename(form.art_slide_image.data.filename)

        file_path1 = os.path.join(current_app.config['UPLOAD_FOLDER'], filename1)
        file_path2 = os.path.join(current_app.config['UPLOAD_FOLDER'], filename2)
        file_path3 = os.path.join(current_app.config['UPLOAD_FOLDER'], filename3)

        form.art_list_image.data.save(file_path1)
        form.art_enlarge_image.data.save(file_path2)
        form.art_slide_image.data.save(file_path3)

        # art = Art()

    else:
        flash_errors(form)
    return render_template('artupdate.html', form=form)


@main.route('/newsupdate.html')
@login_required
def newsupdate():
    return render_template('newsupdate.html')


@main.route('/priceupdate.html')
@login_required
def priceupdate():
    return render_template('priceupdate.html')


@main.route('/changepwd.html', methods=['GET', 'POST'])
@login_required
def changepwd():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.current_password.data):
            current_user.password = generate_password_hash(form.new_password.data)
            db.session.add(current_user)
            db.session.commit()
            logout_user()
            return redirect(url_for('main.login'))
        else:
            flash(u'原密码错误')

    else:
        flash_errors(form)
    return render_template('changepwd.html', form=form)


@main.route('/login.html', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.update'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(request.values.get('next') or url_for('main.update'))
        else:
            flash(u'用户名或密码错误!')
    else:
        flash_errors(form)

    return render_template('login.html', form=form)


@main.route('/register.html', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('main.login'))
    else:
        flash_errors(form)
    return render_template('register.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


# @main.app_errorhandler(404)
# def page_not_found(e):
#     return render_template('error.html'), 404


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            print(getattr(form, field).label.text, error)
            flash(u'%s - %s' % (getattr(form, field).label.text, error), 'error')
