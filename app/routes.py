from app import app
from app.models import User
from app.forms import LoginForm

from werkzeug.urls import url_parse
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required


@app.route('/')
def hello_page():
    name = current_user.username if current_user.is_authenticated else 'Anonimus User'
    return f'Hello World {name}'


@app.route('/index')
@login_required
def index():
    projects = [
        {
            'id': 1,
            'tutor': {'username': 'Yaron'},
            'team': [{'username': 'Shteren'}, {'username': 'Nathan'}],
            'description': 'Locker manager website'
        },
        {
            'id': 2,
            'tutor': {'username': 'Boaz'},
            'team': [{'username': 'Nati'}, {'username': 'Shteren'},  {'username': 'Nathan'}],
            'description': 'Autonumus Arduino project'
        }
    ]

    return render_template('index.html', title='Home', user=current_user, projects=projects)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user is None:
            flash('Invalid user')
            return redirect(url_for('login'))
        elif not user.check_password(form.password.data):
            flash('Invalid password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
    from getmac import get_mac_address as gma

