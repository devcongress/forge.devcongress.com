import os
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from flask import (
    Flask,
    render_template,
    request
)


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('application.html')


@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        hacker = Hacker.from_forms(request.form)
        return str(hacker)
    else:
        return render_template('apply.html')


@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/teach')
def teach():
    if request.method == 'GET':
        return render_template('teach.html')
    else:
        pass


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

# Models, models.
class Hacker(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Personal.
    email = db.Column(db.String, unique=True, nullable=False)
    phone = db.Column(db.String, unique=True, nullable=False)

    # Social.
    github = db.Column(db.String(100), unique=True)
    twitter = db.Column(db.String(100), unique=True)
    linkedin = db.Column(db.String, unique=True)

    # Bio and extras.
    ambition = db.Column(db.Text, nullable=False)
    program = db.Column(db.Text, nullable=False)
    expectation = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __init__(self, github, email, phone,
                 ambition, program, expectation, twitter=None, linkedin=None):
        self.github = github
        self.email = email
        self.phone = phone
        self.ambition = ambition
        self.program = program
        self.expectation = expectation

        if twitter:
            self.twitter = twitter
        if linkedin:
            self.linkedin = linkedin

    @classmethod
    def from_forms(cls, form):
        # Create a new hacker from the form data.
        pass

    def __repr__(self):
        return '<Hacker %r>' % self.github

if __name__ == '__main__':
    app.run(debug=True)
