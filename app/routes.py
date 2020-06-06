from app import app
from app import db
from app.models import User, Item
from app.forms import LoginForm, RegistrarionForm, QuickAddUserForm, AddItemForm

from werkzeug.urls import url_parse
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required


@app.route('/')
def hello_page():
    name = current_user.username if current_user.is_authenticated else 'Anonimus User'
    return f'Hello World {name}'


@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = QuickAddUserForm()
    if form.validate_on_submit():
        quick_add_user(form.name.data)

    all_users = User.query.all()
    return render_template('index.html', title='Home', login_user=current_user, users=all_users, quick_form=form)


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
    form = RegistrarionForm()
    if form.validate_on_submit():
        u = User.new_user(username=form.username.data, email=form.email.data, password=form.password.data)

        db.session.add(u)
        db.session.commit()
        flash(f'Congratulation {u.username}! You were registered successfully!')

        # If next argument exist (and it is relative only) then redirect to it.
        next_page = request.args.get('next')
        if next_page and (not url_parse(next_page).netloc != ''):
            return redirect(next_page)

        # If no user was loged in then redirect to login page
        if not current_user.is_authenticated:
            return redirect(url_for('login'))

    # Else redirect to register page.
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user_description(username):
    u = User.query.filter(User.username == username).first_or_404()
    print(f'Found user: {u} with mail: {u.email}')
    items = [
        {'id': 1, 'description': 'Test Item #1', 'author': u},
        {'id': 2, 'description': 'Test Item #2', 'author': u}
    ]

    return render_template('user.html', user=u, items=items)


@app.route('/delete_user/<username>', methods=['GET', 'POST'])
@login_required
def delete_user(username):
    u = User.query.filter(User.username == username).first_or_404()

    if u == current_user:
        flash(f'Attention {u.username} You cannot remove yourself from the db')
    else:
        db.session.delete(u)
        db.session.commit()
        flash(f'User {u.username} was removed from database')

    return redirect(url_for('index'))


def quick_add_user(username):
    u = User.new_user(username=username, email=f'{username}@{username}.com', password=username)
    db.session.add(u)
    db.session.commit()

    flash(f'Congratulation {u.username}! You were registered successfully!')


@app.route('/all_items')
def all_items():
    items = Item.query.all()
    return render_template('all_items.html', items=items)


@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    form = AddItemForm()
    if form.validate_on_submit():
        item = Item.new_item(title=form.title.data, description=form.description.data)

        db.session.add(item)
        db.session.commit()
        flash(f'Congratulation {item.title}! You were registered successfully!')

        # If next argument exist (and it is relative only) then redirect to it.
        next_page = request.args.get('next')
        if next_page and (not url_parse(next_page).netloc != ''):
            return redirect(next_page)

    # Else redirect to add item page.
    return render_template('add_item.html', title='Add Item', form=form)


@app.route('/item_description/<item_id>')
def item_description(item_id):
    item = Item.query.filter(Item.id == item_id).first_or_404()

    return render_template('item.html', item=item)


@app.route('/delete_item/<item_id>', methods=['GET', 'POST'])
def delete_item(item_id):
    item = Item.query.filter(Item.id == item_id).first_or_404()

    db.session.delete(item)
    db.session.commit()
    flash(f'User {item.title} was removed from database')

    return redirect(url_for('all_items'))


@app.route('/ask_for_item/<item_title>', methods=['GET', 'POST'])
def ask_for_item(item_title):
    try:
        current_user.add_item(item_title)
    except Item.UnavailbleItem:
        flash(f'Item {item_title} is Unavailable at this moment.')
