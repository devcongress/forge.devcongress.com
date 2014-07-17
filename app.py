import os
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from flask import (
   Flask,
   url_for,
   render_template,
   redirect,
   request,
   flash
)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = os.environ.get('DATABASE_URL')

db = SQLAlchemy(app)


@app.route('/')
def home():
    return render_template('application.html')

@app.route('/apply', methods=['GET','POST'])
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


# Models, models.
class Hacker(db.Model):
    id         = db.Column(db.Integer, primary_key=True)

    # Personal.
    nickname   = db.Column(db.String(100), unique=True, nullable=False)
    email      = db.Column(db.String, unique=True, nullable=False)
    phone      = db.Column(db.String, unique=True, nullable=False)

    # Social.
    github     = db.Column(db.String(100), unique=True)
    twitter    = db.Column(db.String(100), unique=True)
    linkedin   = db.Column(db.String, unique=True)

    # Bio and extras.
    ambition   = db.Column(db.Text, nullable=False)
    program    = db.Column(db.Text, nullable=False)
    expectation = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __init__(self, nickname, email, github, twitter=None, linkedin=None):
      self.nickname = nickname
      self.email = email
      self.github = github


    @classmethod
    def from_forms(cls, form):
      # Create a new hacker from the form data.
      pass

    def __repr__(self): return '<Hacker %r>' % self.github

if __name__ == '__main__':
    app.run(debug=True)
