import json
import random
from functools import wraps

from flask import Flask, render_template, request, session, redirect

from WithDB import ConnectDB
from captcha_tools import HCaptcha
from email_tools import EmailTools
from password_tools import PasswordTools
from settings import SetSettings

app = Flask(__name__)
SetSettings('./settings.json', app).use()


def is_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'login' in session and session['login']:
            return func(*args, **kwargs)
        return render_template(app.config['site']['login_page'], **app.config['default']['login_page'])

    return wrapper


@app.route('/')
def home():
    return render_template(app.config['site']['home_page'])
    # return render_template(app.config['site']['home_page'],
    #                        email=session['email'],
    #                        role=session['role'],
    #                        username=session['username'])


@app.route('/log')
def log_():
    if 'login' not in session:
        response = app.config['default']['login_page']
        return render_template(app.config['site']['login_page'], **response)
    else:
        return redirect('/')


@app.route('/login', methods=['post'])
def login():
    email = request.form.get('email')
    passw = request.form.get('password')
    checker = EmailTools(email)
    res = checker.is_valid(app.config['domains'])
    pt = PasswordTools(passw)
    res2 = pt.check_password(8, 40)
    response = app.config['default']['login_page']
    token = request.form.get('h-captcha-response')
    captcha = HCaptcha(token, app.config['secret_key_h'])
    if captcha.verify():
        if res and res2:
            with ConnectDB(app.config['db_path']) as db:
                db.execute('SELECT * FROM users WHERE email=? AND "password"=? LIMIT 1',
                           (email, str(pt.hash())))
                ans = db.fetchall()
                if len(ans):
                    ans = ans[0]
                    with ConnectDB(app.config['db_path']) as db2:
                        db2.execute('SELECT * FROM profile WHERE "id"=? LIMIT 1',
                                    (ans[0] + ans[1],))
                        ans2 = db2.fetchall()
                    ans2 = ans2[0]
                    session['login'] = True
                    session['email'] = ans[1]
                    session['ip'] = request.remote_addr
                    session['username'] = ans[0]
                    session['id'] = ans[3]
                    session['role'] = ans2[4]
                    return redirect('/')
                else:
                    response["error"] = app.config['user_not_found_error']
                    response["email"] = email
        elif not res2:
            response["error"] = app.config['password_error']
            response["email"] = email
        else:
            response["error"] = app.config['email_error']
            response["email"] = email
    else:
        response["error"] = app.config['captcha_error']
        response["email"] = email
    return render_template(app.config['site']['login_page'], **response)


@app.route('/registration')
def registration():
    response = app.config['default']['registration']
    return render_template(app.config['site']['registration'], **response)


@app.route('/reg', methods=['post'])
def reg():
    email = request.form.get('email')
    username = request.form.get('username')
    passw = request.form.get('password')
    passw2 = request.form.get('password2')
    checker = EmailTools(email)
    res = checker.is_valid(app.config['domains'])
    pt = PasswordTools(passw)
    res2 = pt.check_password(8, 40)
    with ConnectDB(app.config['db_path']) as db:
        db.execute('SELECT * FROM users WHERE email=? LIMIT 1', (email,))
        em = db.fetchall()
    us = json.loads(check(username))
    response = app.config['default']['registration']
    token = request.form.get('h-captcha-response')
    captcha = HCaptcha(token, app.config['secret_key_h'])
    if captcha.verify():
        if not res2:
            response["error"] = app.config['password_error']
            response["email"] = email
        elif not res:
            response["error"] = app.config['email_error']
            response["email"] = email
        elif us['res'] != '':
            response["error"] = app.config['username_already_taken']
            response["email"] = email
        elif len(username) < 4 or len(username) > 30:
            response["error"] = app.config['invalid_length_of_username']
            response["email"] = email
        elif len(em):
            return redirect('/')
        elif passw != passw2:
            response["error"] = app.config['password_do_not_match']
            response["email"] = email
        else:
            with ConnectDB(app.config['db_path']) as db:
                db.execute('SELECT * FROM users WHERE username=? LIMIT 1', (username,))
                ans = db.fetchall()
            if len(ans):
                response["error"] = app.config['username_already_taken']
                response["email"] = email
            else:
                session['email'] = email
                session['ip'] = request.remote_addr
                session['username'] = username
                session['try'] = 3
                session['password'] = pt.hash()
                session['code'] = random.randrange(100000, 999999)
                checker.send_email(app.config['subject'], app.config['from'],
                                   render_template('code.html', from_=app.config['from'], code=session['code']),
                                   **app.config['sender'])
                return redirect('/code')
    else:
        response["error"] = app.config['captcha_error']
        response["email"] = email
    return render_template(app.config['site']['registration'], **response)


@app.route('/code')
def code():
    if 'email' in session and 'password' in session and 'username' in session and 'code' in session:
        return render_template(app.config['site']['email_sent'], email=session['email'], submit="submit")
    else:
        return redirect('/registration')


@app.route('/submit', methods=['post'])
def submit():
    if 'try' in session and \
            session['try'] > 0 and \
            'email' in session and \
            'password' in session and \
            'username' in session and \
            'code' in session:
        session['try'] -= 1
        if str(session['code']) == request.form.get('code'):
            with ConnectDB(app.config['db_path']) as db:
                db.execute('INSERT INTO users VALUES (?, ?, ?, ?)', (
                    session['username'],
                    session['email'],
                    str(session['password']),
                    session['username'] + session['email']
                ))
            with ConnectDB(app.config['db_path']) as db:
                db.execute('INSERT INTO profile VALUES (?, ?, ?, ?, ?)', (
                    session['username'] + session['email'],
                    'static/user.svg',
                    '',
                    '',
                    'user'
                ))
            return redirect('/')
        else:
            return render_template(app.config['site']['email_sent'], email=session['email'], submit="submit")
    else:
        return redirect('/registration')


@app.route('/username/<username>')
def check(username):
    with ConnectDB(app.config['db_path']) as db:
        db.execute('SELECT username FROM users WHERE username=? LIMIT 1', (username,))
        ans = db.fetchall()
    if len(ans):
        return json.dumps({'res': app.config['username_already_taken']})
    else:
        return json.dumps({'res': ''})


@app.route('/reset')
def reset():
    return render_template(app.config['site']['reset_page'], **app.config['default']['reset'])


@app.route('/res', methods=['post'])
def res():
    token = request.form.get('h-captcha-response')
    captcha = HCaptcha(token, app.config['secret_key_h'])
    response = app.config['default']['reset']
    checker = EmailTools(request.form.get('email'))
    if captcha.verify():
        with ConnectDB(app.config['db_path']) as db:
            db.execute('SELECT * FROM users WHERE email=? LIMIT 1',
                       (request.form.get('email'),))
            ans = db.fetchall()
            if len(ans):
                session['email'] = request.form.get('email')
                session['try'] = 3
                session['code'] = random.randrange(100000, 999999)
                checker.send_email(app.config['subject'], app.config['from'],
                                   render_template('code.html', from_=app.config['from'], code=session['code']),
                                   **app.config['sender'])
        return render_template(app.config['site']['email_sent'], submit="change",
                               email=request.form.get('email'))
    else:
        response["error"] = app.config['captcha_error']
    return render_template(app.config['site']['reset_page'], **response)


@app.route('/change', methods=['post'])
def change():
    code = request.form.get('code')
    if 'email' in session and 'try' in session and session['try'] > 0:
        session['try'] -= 1
        if code == str(session['code']):
            session['checked'] = True
            return render_template(app.config['site']['change'])
        else:
            return render_template(app.config['site']['email_sent'], submit="change",
                                   email=session['email'])
    return redirect('/reset')


@app.route('/saveChanges', methods=['post'])
def save_changes():
    passw = request.form.get('passw')
    passw2 = request.form.get('passw2')
    checker = PasswordTools(passw)
    if passw == passw2 and checker.check_password(8, 40) and 'email' in session and 'try' in session and \
            session['try'] >= 0 and 'code' in session and 'checked' in session and session['checked']:
        with ConnectDB(app.config['db_path']) as db:
            db.execute('UPDATE users SET password=? WHERE email=?',
                       (str(checker.hash()), session['email']))
        resp = app.config['default']['login_page']
        resp['error'] = app.config['password_changed']
        resp['email'] = session['email']
        return render_template(app.config['site']['login_page'], **resp)
    else:
        return render_template(app.config['site']['change'],
                               error=app.config['password_do_not_match'])


if __name__ == '__main__':
    app.run()
