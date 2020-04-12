from app import app
from app import db
from app.models import User
from app.forms import LoginForm, RegistrarionForm

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


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrarionForm()
    if form.validate_on_submit():
        u = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        db.session.add(u)
        db.session.commit()
        flash(f'Congratulation {u.username}! You were registered successfully!')

        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    u = User.query.filter(User.username == username).first_or_404()
    print(f'Found user: {u} with mail: {u.email}')
    items = [
        {'id': 1, 'description': 'Test Item #1', 'author': u},
        {'id': 2, 'description': 'Test Item #2', 'author': u}
    ]

    return render_template('user.html', user=u, items=items)
