import os
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask.ext.mail import Mail, Message
from threading import Thread
from flask import (
    Flask,
    render_template,
    request,
    jsonify
)


app = Flask(__name__)
app.secret_key = os.environ['FORGE_SECRET_KEY']
app.config.from_object(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            contact = Contact.from_forms(request.form)
            print contact
            db.session.add(contact)
            db.session.commit()
            details = {"name": contact.fullname,
                       "email": contact.email,
                       "phone": contact.phone
                       }
            send_email(app.config['MAIL_SENDER'], ' Enquiry', 'enquiry_mail',
                       **details)
            message = {
                'success': True,
                'msg': 'Awesome! Watch out for more information about the program'
            }
            return jsonify(message)
        except IntegrityError:
            message = {
                'success': False,
                'msg': 'Oops. This email address has already been registered.'
            }
            return jsonify(message)

    else:
        return render_template('application.html')


@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        try:
            hacker = Hacker.from_forms(request.form)
            print hacker
            db.session.add(hacker)
            db.session.commit()
            send_email(hacker.email, " Application", "mail/welcome", name=hacker.fullname)
            message = {
                'success': True,
                'msg': 'Awesome! You should receive an email confirmation immediately'
            }
            return jsonify(message)
        except IntegrityError:
            message = {
                'success': False,
                'msg': 'Oops. This email address has already been registered.'
            }
            return jsonify(message)
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
    fullname = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)

    # Social.
    github = db.Column(db.String(100), unique=True)
    twitter = db.Column(db.String(100), unique=True)
    linkedin = db.Column(db.String(100), unique=True)

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


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, fullname, email, phone):
        self.fullname = fullname
        self.email = email
        self.phone = phone

    @classmethod
    def from_forms(cls, form):
        return Contact(**{
            k: v if len(v.strip()) else None for k, v in form.items() if k != 'submit'
        })

    def __repr__(self):
        return '<Contact %r (%r)>' % (self.fullname, self.email)


# mail configs
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
app.config['MAIL_SUBJECT_PREFIX'] = '[Forge]'
app.config['MAIL_SENDER'] = os.environ['MAIL_USERNAME']

mail = Mail(app)


def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

if __name__ == '__main__':
    app.run(debug=True)
