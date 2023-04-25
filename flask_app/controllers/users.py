from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from flask_app.models import user

bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return redirect ('/login')

@app.route('/login')
def login_reg():
    # if session.get('user_id'):
    #     return redirect ('/dashboard')
    return render_template ('login_reg.html')

@app.route('/login-register', methods=['POST'])
def register_user():
    if not user.User.validate_registration(request.form):
        session['first_name'] = request.form.get('first_name')
        session['last_name'] = request.form.get('last_name')
        session['email'] = request.form.get('email')
        return redirect ('/login')
    data = {
        'email': request.form.get('email')
    }
    user_in_db = user.User.get_by_email(data)
    if user_in_db:
        session['first_name'] = request.form.get('first_name')
        session['last_name'] = request.form.get('last_name')
        session['email'] = request.form.get('email')
        flash('This email is already associated with an account. Please try logging in with this email or creating an account with a different email.', 'email')
        return redirect ('/login')
    if not user_in_db:
        if session:
            session.clear()
        pw_hash = bcrypt.generate_password_hash(request.form.get('password'))
        data = {
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name'),
            'email': request.form.get('email'),
            'password': pw_hash
        }
        session['user_id'] = user.User.create_user(data)
        return redirect ('/dashboard')

@app.route('/login-login', methods=['POST'])
def login_user():
    data = {
        'email': request.form.get('login_email')
    }
    user_in_db = user.User.get_by_email(data)
    if not user_in_db:
        session['login_email'] = request.form.get('login_email')
        flash('Invalid login attempt!', 'login')
        return redirect ('/login')
    if not bcrypt.check_password_hash(user_in_db.password, request.form.get('login_password')):
        session['login_email'] = request.form.get('login_email')
        flash('Invalid login attempt!', 'login')
        return redirect ('/')
    session.clear()
    session['user_id'] = user_in_db.id
    return redirect ('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect ('/login')