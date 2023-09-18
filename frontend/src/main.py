"""
По адресу http://127.0.0.1:5000/ доступна форма для отправки обращения.
"""

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def display_form():
    return render_template('form.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
