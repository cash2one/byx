from . import main
from flask import render_template

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
    return render_template('exhibition.html')