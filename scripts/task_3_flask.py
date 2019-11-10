import csv
import hashlib
import time
from random import randint, seed

import pendulum
from flask import Flask, redirect, render_template, request, url_for

from task_2 import *

app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for('infoform'))


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
    message = None
    if request.method == 'POST':
        would_log_in = valid_login(request.form['email'], request.form['password'])
        timeout = get_timeout(request.form['email'], would_log_in)
        if pendulum.now('UTC') > timeout:
            if would_log_in:
                message = 'You would log in succesfully'
            else:
                error = 'Invalid username/password'
        else:
            error = 'You have been locked out, you can log in again in {num} minutes'.format(num=(timeout - pendulum.now('UTC')).in_minutes()+1)

    return render_template('login.html', error=error, message=message, email=request.form.get('email', default=None))


def valid_password(password):
    if len(password) < 3:
        return False, "This password is too short."
    password_dict = {
        'dictionary': {},
        'info': {},
    }
    with open('./ELCP-1.txt') as f, open('./ELCP-2.txt') as f2:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            try:
                password_dict['dictionary'][row[0]].append(row[1])
            except KeyError:
                password_dict['dictionary'][row[0]] = []
                password_dict['dictionary'][row[0]].append(row[1])
        f.close()

        reader = csv.reader(f2, delimiter=',')
        for row in reader:
            try:
                password_dict['info'][row[0]].append(row[1])
            except KeyError:
                password_dict['info'][row[0]] = []
                password_dict['info'][row[0]].append(row[1])
        f2.close()
    
    for key, lst in password_dict['dictionary'].items():
        if password.lower() in lst:
            return False, "\"Your password is vulnerable to dictionary attack since you used the dictionary word: '{}', or a variation of this word in your password\"".format(key)
    for key, lst in password_dict['info'].items():
        if password.lower() in lst:
            return False, "Your password is vulnerable to targeted guessing attack since you used your {} or a part of it in your password".format(key)
    return True, ""


def log_the_user_in():
    pass


def storePassword(email, password):
    digest, salt = hash_pass(password)

    hash_digest = open("hash_digest.txt", "a+")
    hash_digest.write('{}, {}\n'.format(email.lower().strip(), digest.strip()))
    salt_file = open("salt.txt", "a+")
    salt_file.write('{}, {}\n'.format(email.lower().strip(), str(salt)))
    hash_digest.close()
    salt_file.close()


def hash_pass(password, salt=None):
    if salt is None:
        seed(time.time())
        salt = randint(100000, 99999999999)
    password += str(salt)

    m = hashlib.new("sha256")
    m.update(password.encode())
    return m.hexdigest(), salt


def valid_login(email, password):
    hash_dict = get_hash_dict(email, password)

    user_salt = ''
    user_digest = ''
    try:
        tmphash = hash_dict[email].split('.')
        user_salt = tmphash[0]
        user_digest = tmphash[1]
    except KeyError:
        return False

    test_digest, _ = hash_pass(password, salt=user_salt)
    if test_digest == user_digest:
        return True
    return False


def get_hash_dict(email, password):
    """
    Reads in dictionary of hashes and salts. Final stored format is '<salt>.<hash>'
    """
    hash_dict = {}
    with open('hash_digest.txt', 'r') as hashfile, open('salt.txt', 'r') as saltfile:
        salt_reader = csv.reader(saltfile)
        for row in salt_reader:
            hash_dict[row[0]] = row[1].strip()
        saltfile.close()
        hash_reader = csv.reader(hashfile)
        for row in hash_reader:
            hash_dict[row[0]] = '{salt}.{hash}'.format(salt=hash_dict[row[0]], hash=row[1].strip())
        hashfile.close()
    return hash_dict


def get_timeout(email, login_success):
    email = email.lower().strip()
    timeout_until = pendulum.now('UTC').to_iso8601_string()
    attempts = 0

    # Get timeout dictionary [email, timeout_until, attempts]
    file_dict = read_timeout_dict()

    # If user exists
    if file_dict.get(email):
        timeout_until = file_dict[email][0]
        attempts = int(file_dict[email][1])
    # Not in file yet
    else:
        file_dict[email] = [timeout_until, attempts]

    # Only reset attempts if we're not locked out.
    if login_success and not is_locked_out(timeout_until):
        attempts = 0
        file_dict[email] = [timeout_until, attempts]
    # Login unsuccessful
    else:
        if not is_locked_out(timeout_until):
            attempts += 1
            if attempts % 3 == 0:
                #  Timeout = 2^n seconds where n = (attempts % 3) - 1 = {0, 1, 2, 3, ...}
                file_dict[email][0] = pendulum.now('UTC').add(minutes=((2**((attempts//3)-1)))).to_iso8601_string()
            file_dict[email][1] = attempts
    # Write back to disk and return timeout value
    write_timeout_dict_to_file(file_dict)
    return pendulum.parse(file_dict[email][0])


def is_locked_out(timeout_until):
    if type(timeout_until) == str:
        return pendulum.now('UTC') < pendulum.parse(timeout_until)
    else:
        return pendulum.now('UTC') < timeout_until


def read_timeout_dict():
    file = {}
    try:
        with open('last_failed.txt', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                file[row[0]] = [row[1], row[2]]
            f.close()
    except FileNotFoundError:
        pass
    return file


def write_timeout_dict_to_file(file_dict):
    with open('last_failed.txt', 'w') as f:
        writer = csv.writer(f)
        for key, lst in file_dict.items():
            writer.writerow([key, lst[0], lst[1]])
        f.close()


if __name__ == '__main__':
    import os
    os.environ["FLASK_ENV"] = "development"
    app.run(debug=True)
