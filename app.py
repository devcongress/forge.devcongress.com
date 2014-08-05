import os
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for
)


app = Flask(__name__)
app.secret_key = os.environ['FORGE_SECRET_KEY']
app.config.from_object(__name__)

@app.route('/')
def home():
    return render_template('application.html')


@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        try:
            hacker = Hacker.from_forms(request.form)
            print hacker
            db.session.add(hacker)
            db.session.commit()
            flash('Awesome! You should receive an email confirmation immediately')
            return redirect(url_for('home'))
        except IntegrityError as e:
            print e
            flash('Oops. This email address has already been registered.')
            return render_template('apply.html')
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
if not app.config['SQLALCHEMY_DATABASE_URI']:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['FORGE_DATABASE_URL']

db = SQLAlchemy(app)


# Models, models.
class Hacker(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Personal.
    fullname = db.Column(db.String, nullable=False)
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


    def __init__(self, fullname, github, email, phone,
                 ambition, program, expectation, twitter=None, linkedin=None):
        self.fullname = fullname
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
        return Hacker(**{
            k: v if len(v.strip()) else None for k, v in form.items() if k != 'submit'
        })

    def __repr__(self):
        return '<Hacker %r (%r)>' % (self.fullname, self.github)



if __name__ == '__main__':
    app.run(debug=True)
