"""
При запуске файла по адресу http://127.0.0.1:5000/ становится доступна форма для отправки обращения.
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('form.html')


if __name__ == '__main__':
    print('hi')
    app.run(host='0.0.0.0')
