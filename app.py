from flask import Flask, url_for, render_template, redirect, request, flash

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('application.html')


@app.route('/apply', methods=['GET', 'POST'])
def apply():
    return render_template('apply.html')


@app.route('/faq', methods=['GET'])
def faq():
    return render_template('faq.html')


if __name__ == '__main__':
    app.run(debug=True)
