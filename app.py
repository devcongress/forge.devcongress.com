from flask import (
                   Flask,
                   url_for,
                   render_template,
                   redirect,
                   request,
                   flash
                  )

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('application.html')

if __name__ == '__main__':
    app.run(debug=True)
