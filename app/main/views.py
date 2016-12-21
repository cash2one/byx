from . import main
from flask import render_template, request
from ..models import News


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


@main.route('/changepwd.html')
def changepwd():
    return render_template('changepwd.html')
