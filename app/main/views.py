# coding:utf8
from . import main
from flask import render_template, request, redirect, url_for, flash, current_app, jsonify
from ..models import News, User, Artist, Art, Branch, ArtType, Price
from flask_login import current_user, login_user, login_required, logout_user
from .forms import LoginForm, RegisterForm, ChangePasswordForm, ArtistForm, ArtForm, NewsForm, PriceForm
from werkzeug.security import check_password_hash, generate_password_hash
from .. import db
import os
import time
from .utils import random_file_name
from sqlalchemy import or_
import datetime


@main.route('/')
def index():
    artistlist = Artist.query.all()

    # 首页轮播取最多6个倒序
    life_list = Art.query.filter(Art.type == 8).filter(Art.index_slider_image != '').filter(
        Art.index_life_image != '').order_by(Art.created.desc()).limit(6).all()

    return render_template('index3.html', artistlist=artistlist, life_list=life_list)


@main.route('/about.html')
def about():
    return render_template('about_1.html')


@main.route('/byx_list.html')
def byx_list():
    branch_id = request.args.get('branch', 0, type=int)

    branch = Branch.query.filter(Branch.branch_id == branch_id).first_or_404()
    newslist = News.query.filter(News.category == branch_id).all()
    return render_template('byx_list.html', newslist=newslist, branch=branch)


@main.route('/byx_details.html')
def byx_detail():
    detail_id = request.args.get('detail_id', 1, type=int)
    branch_id = request.args.get('branch', 0, type=int)
    news = News.query.filter(News.id == detail_id).filter(News.category == branch_id).first_or_404()
    return render_template('byx_details.html', news=news)


@main.route('/artist.html')
def artist():
    artistlist = Artist.query.all()
    return render_template('artistlist.html', artistlist=artistlist)


@main.route('/artistlive/<int:id>.html')
def artistlive(id):
    artist = Artist.query.filter(Artist.id == id).first_or_404()

    artistlist = Artist.query.filter(Artist.id == id).join(Art, Artist.id == Art.artist_id).add_columns(
        Art.art_list_image, Art.id, Art.name).all()
    return render_template('artistlive.html', artistlist=artistlist, artist=artist)


@main.route('/artlist.html')
def artlist():
    type_id = request.args.get('type', 1, type=int)
    artlist = Art.query.filter(Art.type == type_id).all()
    return render_template('artlist.html', artlist=artlist)


@main.route('/artlive/<int:id>.html')
def artlive(id):
    artlive = Art.query.filter(Art.id == id).filter(Art.index_life_image != '').join(Artist,
                                                                                     Art.artist_id == Artist.id).add_columns(
        Artist.name, Artist.avatar).first_or_404()
    life_images = [x for x in artlive.Art.life_image.split(';') if x]
    return render_template('artlive.html', artlive=artlive, life_images=life_images)


@main.route('/artlives.html')
def artlives():
    type = request.args.get('type', 0, type=int)
    art_type = ArtType.query.filter(ArtType.type_id == type).first_or_404()
    artlist = Art.query.filter(Art.type == type).all()
    return render_template('artlives.html', artist=artlist, art_type=art_type)


@main.route('/artshow/<int:id>.html')
def artshow(id):
    art_detail = Art.query.filter(Art.id == id).join(Artist, Art.artist_id == Artist.id).add_columns(Artist.name,
                                                                                                     Artist.location,
                                                                                                     Artist.introduction,
                                                                                                     Artist.avatar
                                                                                                     ).first_or_404()
    artist_id = art_detail.Art.artist_id
    art_list = Art.query.filter(Art.artist_id == artist_id).filter(Art.id != id).all()
    # todo
    price_list = [{'art_price': i.art_price, 'sale_time': i.sale_time} for i in
                  Price.query.filter(Price.art_id == id).all()]
    price_list.sort(key=lambda x: datetime.datetime.strptime(x['sale_time'], '%Y-%m-%d'))
    return render_template('artshow2.html', art_detail=art_detail, art_list=art_list)


@main.route('/update.html', methods=['GET', 'POST'])
@login_required
def update():
    return render_template('update.html')


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

    artistlist = Artist.query.order_by(Artist.created.desc()).all()
    return render_template('artistupdate.html', form=form, artistlist=artistlist)


@main.route('/artist/delete/<int:id>', methods=['GET', 'POST'])
def delete_artist(id):
    have_artist = Artist.query.filter_by(id=id).first_or_404()
    db.session.delete(have_artist)
    db.session.commit()
    return redirect(request.referrer or url_for('main.artistupdate'))


@main.route('/artupdate.html', methods=["GET", "POST"])
@login_required
def artupdate():
    form = ArtForm()
    if form.validate_on_submit():

        name = form.name.data
        introduction = form.introdution.data
        subtitle = form.subtitle.data
        type_id = form.type.data
        artist_id = form.artist_id.data

        art_list_image_filename = random_file_name(form.art_list_image.data.filename)
        art_enlarge_image_filename = random_file_name(form.art_enlarge_image.data.filename)
        art_slide_image_filename = random_file_name(form.art_slide_image.data.filename)

        art_list_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], art_list_image_filename)
        art_enlarge_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], art_enlarge_image_filename)
        art_slide_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], art_slide_image_filename)

        form.art_list_image.data.save(art_list_image_path)
        form.art_enlarge_image.data.save(art_enlarge_image_path)
        form.art_slide_image.data.save(art_slide_image_path)

        # 走进生活
        if form.life_image.data:
            index_images = request.files.getlist("life_image")
            if index_images:
                life_image_filename = ''
                for each in index_images:
                    each_life_image_filename = random_file_name(each.filename)
                    each_life_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], each_life_image_filename)
                    each.save(each_life_image_path)
                    life_image_filename += each_life_image_filename + ';'
                if life_image_filename:
                    index_life_image_filename = life_image_filename.split(';')[0]
                    life_image_filename = ';'.join(life_image_filename.split(';')[1:])
                else:
                    life_image_filename = ''
                    index_life_image_filename = ''
        else:
            life_image_filename = ''
            index_life_image_filename = ''

        if form.index_slider_image.data:
            index_slider_image_filename = random_file_name(form.index_slider_image.data.filename)
            index_slider_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], index_slider_image_filename)
            form.index_slider_image.data.save(index_slider_image_path)
        else:
            index_slider_image_filename = ''

        created = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        art = Art(name=name, introduction=introduction, subtitle=subtitle,
                  art_list_image=art_list_image_filename, art_enlarge_image=art_enlarge_image_filename,
                  art_slide_image=art_slide_image_filename,
                  type=type_id, created=created, artist_id=artist_id,
                  index_slider_image=index_slider_image_filename,
                  life_image=life_image_filename,
                  index_life_image=index_life_image_filename)
        db.session.add(art)
        db.session.commit()
        return redirect(url_for("main.artupdate"))

    else:
        flash_errors(form)
    artlist = Art.query.join(Artist, Art.artist_id == Artist.id).add_columns(Artist.name).order_by(
        Art.created.desc()).all()
    return render_template('artupdate.html', form=form, artlist=artlist)


@main.route('/art/delete/<int:id>', methods=['GET', 'POST'])
def delete_art(id):
    have_art = Art.query.filter_by(id=id).first_or_404()
    db.session.delete(have_art)
    db.session.commit()
    return redirect(request.referrer or url_for('main.artupdate'))


@main.route('/newsupdate.html', methods=['GET', 'POST'])
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

    news_list = News.query.all()
    return render_template('newsupdate.html', form=form, news_list=news_list)


@main.route('/news/delete/<int:id>', methods=['GET', 'POST'])
def delete_news(id):
    have_news = News.query.filter_by(id=id).first_or_404()
    db.session.delete(have_news)
    db.session.commit()
    return redirect(request.referrer or url_for('main.newsupdate'))


@main.route('/priceupdate.html', methods=['GET', 'POST'])
@login_required
def priceupdate():
    arts_name = request.args.get('arts_name', '')
    type_id = request.args.get('type_id', -1, type=int)
    artists_id = request.args.get('artists_id', -1, type=int)

    form = PriceForm(type_id, artists_id, arts_name)
    if form.validate_on_submit():
        art_id = form.art_id.data
        art_price = form.price.data
        sale_time = form.sale_time.data
        price = Price(art_id=art_id, art_price=art_price, sale_time=sale_time)
        db.session.add(price)
        db.session.commit()
        return redirect(url_for("main.priceupdate"))
    else:
        flash_errors(form)

    artist_list = Artist.query.all()
    price_list = Price.query.join(Art, Price.art_id == Art.id).join(Artist, Art.artist_id == Artist.id).add_columns(
        Art.name.label('art_name'), Artist.name.label('artist_name'), Art.type, Art.art_list_image).all()
    return render_template('priceupdate.html', form=form, artist_list=artist_list, price_list=price_list)


@main.route('/price/delete/<int:id>', methods=['GET', 'POST'])
def delete_price(id):
    have_price = Price.query.filter_by(id=id).first_or_404()
    db.session.delete(have_price)
    db.session.commit()
    return redirect(request.referrer or url_for('main.priceupdate'))


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


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            if error == u'This field is required.':
                error = u'未填或未选择'
            flash(u'%s - %s' % (getattr(form, field).label.text, error), 'error')


@main.route('/test')
def test():
    return render_template('artist2.html')


# api

@main.route('/price_search', methods=['GET', 'POST'])
@login_required
def price_search():
    artist_id = request.args.get('artist_id', None, type=int)
    art_name = request.args.get('art_name', None)
    type_id = request.args.get('type', None, type=int)
    if artist_id and art_name and type_id:
        result = Artist.query.filter(Artist.id == artist_id).join(Art, Artist.id == Art.artist_id).filter(
            Art.name.like(u'%{}%'.format(art_name))).filter(Art.type == type_id).add_columns(Art.name, Art.type,
                                                                                             Art.art_list_image,
                                                                                             Art.id).all()
        if result:
            rawl_html = ''
            for each in result:
                print type(each.name)
                rawl_html += u'<div class="col-sm-6 col-md-3">' + u'<div class="thumbnail"><img src="/static/upload/' + each.art_list_image + u'" alt="缩略图"><div class="caption"><h4>' + each.name + u'</h4><p>' + each.Artist.name + u'</p><p>' + str(
                    each.type) + u'</p><p><label class="checkbox-inline">' + u'<input type="radio" name="art_id" value="' + str(
                    each.id) + u'">选取</label></p></div></div></div>'
            return jsonify({'status': 1, 'message': rawl_html})
        else:
            return jsonify({'status': 0, 'message': u'无结果'})
    return jsonify({'status': 0, 'message': u'参数未填全'})


@main.route('/search.html', methods=['GET', 'POST'])
def search():
    type = request.args.get('type', 1, type=int)
    keyword = request.args.get('keyword', '')
    if type and keyword:
        if type == 1:
            # search_list = Art.objects.filter(Q)
            search_list = Art.query.filter(
                or_(
                    Art.name.like(u'%{}%'.format(keyword)),
                    Art.subtitle.like(u'%{}%'.format(keyword)),
                    Art.introduction.like(u'%{}%'.format(keyword)),
                )
            ).all()
        elif type == 2:
            search_list = Artist.query.filter(
                or_(
                    Artist.introduction.like(u'%{}%'.format(keyword)),
                    Artist.location.like(u'%{}%'.format(keyword)),
                    Artist.pinyin.like(u'%{}%'.format(keyword)),
                )
            ).all()
        elif type == 3 or type == 4:
            search_list = News.query.filter(
                or_(
                    News.title.like(u'%{}%'.format(keyword)),
                    News.content.like(u'%{}%'.format(keyword)),
                    News.overview.like(u'%{}%'.format(keyword)),
                    News.image_illustrate.like(u'%{}%'.format(keyword)),
                )
            ).all()
        else:
            search_list = ''
        return render_template('search.html', search_list=search_list)

    return render_template('search.html')
