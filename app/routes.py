from app import app
from app.forms import LoginForm
from flask import render_template, flash, redirect


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Nathan'}

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

    return render_template('index.html', title='Home', user=user, projects=projects)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for use: {form.username.data} remember_me: {form.remember_me.data}')
        return redirect('/index')

    return render_template('login.html', title='Sign In', form=form)
