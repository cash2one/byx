# coding:utf8
from . import main
from flask import render_template, request, redirect, url_for, flash, current_app, abort
from ..models import News, User, Artist, Art
from flask_login import current_user, login_user, login_required, logout_user
from .forms import LoginForm, RegisterForm, ChangePasswordForm, SlidePicForm, ArtistForm, ArtForm, NewsForm
from werkzeug.security import check_password_hash, generate_password_hash
from .. import db
import os
import time
from .utils import random_file_name


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
    artistlist = Artist.query.all()
    return render_template('artistlist.html', artistlist=artistlist)


@main.route('/artistlive/<id>.html')
def artistlive(id):
    artistlist = Artist.query.filter(Artist.id == id).join(Art, Artist.id == Art.artist_id).add_columns(
        Art.art_list_image, Art.id, Art.name).all()
    if not artistlist:
        abort(404)
    return render_template('artistlive.html', artist=artistlist)

@main.route('/artlist.html')
def artlist():

    return render_template('artlist.html')


@main.route('/artlive/<id>.html')
def artlive(id):
    artlive = Art.query.filter(Art.id == id).filter(Art.index_life_image != '').join(Artist,
                                                                                     Art.artist_id == Artist.id).add_columns(
        Artist.name, Artist.avatar).first_or_404()
    life_images = [x for x in artlive.Art.life_image.split(';') if x]
    return render_template('artlive.html', artlive=artlive, life_images=life_images)


@main.route('/artshow/<id>.html')
def artshow(id):
    art_detail = Art.query.filter(Art.id == id).join(Artist, Art.artist_id == Artist.id).add_columns(Artist.name,
                                                                                                     Artist.location,
                                                                                                     Artist.introduction,
                                                                                                     Artist.avatar
                                                                                                     ).first_or_404()
    artist_id = art_detail.Art.artist_id
    art_list = Art.query.filter(Art.artist_id == artist_id).filter(Art.id != id).all()
    return render_template('artshow2.html', art_detail=art_detail, art_list=art_list)


@main.route('/exhibition.html')
def exhibition():
    id = request.args.get('id', '')
    if id:
        news = News.query.filter_by(id=id).first()
        return render_template('exhibition.html', news=news)
    else:
        print 'liebiao'


@main.route('/list.html')
def list_page():
    pass


@main.route('/update.html', methods=['GET', 'POST'])
@login_required
def update():
    return render_template('update.html')


@main.route('/sliderpic.html', methods=['GET', 'POST'])
@login_required
def sliderpic():
    form = SlidePicForm()
    if form.validate_on_submit():
        filename1 = random_file_name(form.slider.data.filename)
        filename2 = random_file_name(form.slider_live.data.filename)

        file_path1 = os.path.join(current_app.config['UPLOAD_FOLDER'], filename1)
        file_path2 = os.path.join(current_app.config['UPLOAD_FOLDER'], filename2)
        form.slider.data.save(file_path1)
        form.slider_live.data.save(file_path2)

        return redirect(url_for("main.sliderpic"))
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
        filename1 = random_file_name(form.avatar.data.filename)
        filename2 = random_file_name(form.slide_image.data.filename)
        filename3 = random_file_name(form.list_image.data.filename)

        file_path1 = os.path.join(current_app.config['UPLOAD_FOLDER'], filename1)
        file_path2 = os.path.join(current_app.config['UPLOAD_FOLDER'], filename2)
        file_path3 = os.path.join(current_app.config['UPLOAD_FOLDER'], filename3)

        form.avatar.data.save(file_path1)
        form.slide_image.data.save(file_path2)
        form.list_image.data.save(file_path3)
        created = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        artist = Artist(location=location, name=name, pinyin=pinyin,
                        avatar=filename1, introduction=introduction,
                        slide_image=filename2,
                        list_image=filename3, created=created)
        db.session.add(artist)
        db.session.commit()
        return redirect(url_for("main.artistupdate"))

    else:
        flash_errors(form)

    artistlist = Artist.query.all()
    return render_template('artistupdate.html', form=form, artistlist=artistlist)


@main.route('/artupdate.html', methods=["GET", "POST"])
@login_required
def artupdate():
    form = ArtForm()
    if form.validate_on_submit():

        name = form.name.data
        introduction = form.introdution.data
        subtitle = form.subtitle.data
        type = form.type.data
        artist_id = form.artist_id.data

        # filename1 = random_file_name(form.art_list_image.data.filename)
        filename2 = random_file_name(form.art_enlarge_image.data.filename)

        list_filename = ''
        list_image = request.files.getlist('art_list_image')
        if list_image:
            for each in list_image:
                list_image_filename = random_file_name(each.filename)
                list_image_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], list_image_filename)
                each.save(list_image_file_path)
                list_image_filename_s = list_image_filename + ';'
                list_filename += list_image_filename_s


        filename_list = ''
        images = request.files.getlist("art_slide_image")
        if images:
            for each in images:
                m_filename = random_file_name(each.filename)
                m_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], m_filename)
                each.save(m_file_path)
                m_filename_s = m_filename + ';'
                filename_list += m_filename_s

        # 走进生活
        index_images = request.files.getlist("life_image")
        if index_images:
            index_filename = ''
            for index, each in enumerate(index_images):
                if index == 0:
                    index_life_image_filename = random_file_name(each.filename)
                    index_life_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], index_life_image_filename)
                    each.save(index_life_image_path)
                    index_filename_s = index_life_image_filename + ';'
                    index_filename += index_filename_s
                else:
                    life_image_filename = random_file_name(each.filename)
                    life_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], life_image_filename)
                    each.save(life_image_path)
                    index_filename_s = life_image_filename + ';'
                    index_filename += index_filename_s
        else:
            index_filename = ''
            index_life_image_filename = ''

        # file_path1 = os.path.join(current_app.config['UPLOAD_FOLDER'], filename1)
        file_path2 = os.path.join(current_app.config['UPLOAD_FOLDER'], filename2)
        # file_path3 = os.path.join(current_app.config['UPLOAD_FOLDER'], filename3)

        if form.index_slider_image.data:
            filename4 = random_file_name(form.index_slider_image.data.filename)
            file_path4 = os.path.join(current_app.config['UPLOAD_FOLDER'], filename4)
            form.index_slider_image.data.save(file_path4)
        else:
            filename4 = ''

        # form.art_list_image.data.save(file_path1)
        form.art_enlarge_image.data.save(file_path2)
        # form.art_slide_image.data.save(file_path3)
        created = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        art = Art(name=name, introduction=introduction, subtitle=subtitle,
                  art_list_image=list_filename, art_enlarge_image=filename2, art_slide_image=filename_list,
                  type=type, created=created, artist_id=artist_id,
                  index_slider_image=filename4, life_image=index_filename, index_life_image=index_life_image_filename)
        db.session.add(art)
        db.session.commit()
        return redirect(url_for("main.artupdate"))

    else:
        flash_errors(form)
    artlist = Art.query.join(Artist, Art.artist_id == Artist.id).add_columns(Artist.name).order_by(
        Art.created.desc()).all()
    return render_template('artupdate.html', form=form, artlist=artlist)


@main.route('/newsupdate.html')
@login_required
def newsupdate():
    form = NewsForm()
    if form.validate_on_submit():
        category = form.category.data
        title = form.title.data
        source = form.source.data
        overview = form.overview.data
        image_illustrate = form.image_illustrate.data
        content = form.content.data
        template_content = form.template_content.data

        filename1 = random_file_name(form.news_list_image.data.filename)
        filename2 = random_file_name(form.news_detail_image.data.filename)

        file_path1 = os.path.join(current_app.config['UPLOAD_FOLDER'], filename1)
        file_path2 = os.path.join(current_app.config['UPLOAD_FOLDER'], filename2)

        form.news_list_image.data.save(file_path1)
        form.news_detail_image.data.save(file_path2)
        created = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        news = News(category=category, title=title, source=source,
                    overview=overview, news_list_image=filename1,
                    news_detail_image=filename2, image_illustrate=image_illustrate,
                    content=content, template_content=template_content, created=created)
        db.session.add(news)
        db.session.commit()
        return redirect(url_for("main.newsupdate"))
    else:
        flash_errors(form)
    # todo
    # 管理界面
    return render_template('newsupdate.html', form=form)


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


@main.route('/test')
def test():
    return render_template('artist2.html')
