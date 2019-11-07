from flask import Flask, render_template, request
from random import seed
from random import randint
import time
import hashlib

app = Flask(__name__)


@app.route('/infoform')
def run_template():
    return render_template('index.html')

@app.route('/', methods=['POST', 'GET'])
def infoform():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('index.html', error=error)

@app.route('/password', methods=['POST', 'GET'])
def password():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['password']):
            return log_the_user_in()
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('password.html', error=error)

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['password']):
            return log_the_user_in()
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)


password_test = "password123"
seed(time.time())
salt = randint(487564,45729857452974)
password_test += salt

m = hashlib.new("sha512")
m.update(password_test)
m.hexdigest()
