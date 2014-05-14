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

@app.route('/apply', methods=['GET','POST'])
def apply():
		pass

if __name__ == '__main__':
    app.run(debug=True)
