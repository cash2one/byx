# coding:utf8
from . import main
from flask import render_template, request, redirect, url_for, flash
from ..models import News, User
from flask_login import current_user, login_user, login_required, logout_user
from .forms import LoginForm, RegisterForm, ChangePasswordForm
from werkzeug.security import check_password_hash, generate_password_hash
from .. import db


# todo
# http://stackoverflow.com/questions/18600031/changing-the-active-class-of-a-link-with-the-twitter-bootstrap-css-in-python-fla



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


@main.route('/update.html')
@login_required
def update():
    return render_template('update.html')


@main.route('/sliderpic.html')
def sliderpic():
    return render_template('sliderpic.html')


@main.route('/artistupdate.html')
def artistupdate():
    return render_template('artistupdate.html')


@main.route('/artupdate.html')
def artupdate():
    return render_template('artupdate.html')


@main.route('/artupdate2.html')
def artupdate2():
    return render_template('artupdate.html')


@main.route('/priceupdate.html')
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
            print(request.values.get('next'))
            return redirect(request.values.get('next') or url_for('main.update'))
        else:
            flash(u'用户名或密码错误!')
    else:
        flash_errors(form)

    return render_template('login.html', form=form)


@main.route('/register.html', methods=['GET', 'POST'])
def register():
    print(request.args)
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
            flash(u'%s - %s' % (getattr(form, field).label.text, error), 'error')
