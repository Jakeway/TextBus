__author__ = 'jakeway'

from flask import Flask, render_template, request
app = Flask(__name__)
app.config.from_envvar('TextBus_SETTINGS')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/register ', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run()