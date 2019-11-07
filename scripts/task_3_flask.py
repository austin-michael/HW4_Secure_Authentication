from flask import Flask, render_template, request, redirect, url_for
from random import seed
from random import randint
import time
import hashlib
from task_2 import *
import csv

app = Flask(__name__)


@app.route('/infoform')
def run_template():
    return render_template('index.html')


@app.route('/infoform', methods=['POST', 'GET'])
def infoform():
    error = None
    if request.method == 'POST':
        gen_file(first_name=request.form['fName'], last_name=request.form['lName'], date_of_birth=request.form['bDay'], telephone_number=request.form['phone'],
                 street=request.form['street'], apt_num=request.form['aptNum'], city=request.form['city'], state=request.form['state'], zip_code=request.form['zip'], email=request.form['email'])
        return redirect(url_for('password', email=request.form['email'], **request.args))
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('index.html', error=error)


@app.route('/password', methods=['POST', 'GET'])
def password():
    error = None
    if request.method == 'POST':
        pw_valid, error = valid_password(request.form['password'])
        if pw_valid:
            storePassword(request.form['email'], request.form['password'])
            return redirect(url_for('login'))
    return render_template('password.html', error=error, email=request.args.get('email', default=''))
    # the code below is executed if the request method
    # was GET or the credentials were invalid


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


def valid_password(password):
    password_list = []
    with open('./ELCP-1.txt') as f, open('./ELCP-2.txt') as f2:
        reader = csv.reader(f)
        temp_list = []
        for row in reader:
            temp_list.append(row[0])
        f.close()

        password_list.append(temp_list)

        reader = csv.reader(f2)
        temp_list = []
        for row in reader:
            temp_list.append(row[0])
        f2.close()

        password_list.append(temp_list)

    if password in password_list[0]:
        return False, "“Your password is vulnerable to dictionary attack since you used the dictionary word: '{}', or a variation of this word in your password” ".format(password)
    if password in password_list[1]:
        return False, "Your password is vulnerable to targeted guessing attack since you used your personal information or a part of it in your password"
    return True, ""


def log_the_user_in():
    pass

def storePassword(email, password):
    seed(time.time())
    salt = randint(487564, 45729857452974)
    password += str(salt)

    m = hashlib.new("sha256")
    m.update(password.encode())

    hash_digest = open("hash_digest.txt", "a+")
    hash_digest.write('{}, {}\n'.format(email, m.hexdigest()))
    salt_file = open("salt.txt", "a+")
    salt_file.write('{}, {}\n'.format(email, str(salt)))






# if __name__ == '__main__':
app.run(debug=True)
