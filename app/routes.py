from app import app
from flask import render_template


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
