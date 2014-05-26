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
  if request.method == 'GET':
    return render_template('apply.html')
  else:
    pass

@app.route('/faq')
def faq():
  return render_template('faq.html')

@app.route('/teach')
def teach():
  if request.method == 'GET':
    return render_template('teach.html')
  else:
    pass

@app.route('/program')
def program():
  if request.method == 'GET':
    return render_template('program.html')
  else:
    pass

if __name__ == '__main__':
    app.run(debug=True)
