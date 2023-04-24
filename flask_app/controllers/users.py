from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
from flask_app.models.player import Player
bcrypt = Bcrypt(app)


@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    print(request.form)
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "id" : request.form["id"],
        "firstname": request.form["firstname"],
        "lastname" : request.form["lastname"],
        "email" : request.form["email"],
        "password" : pw_hash
        }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/dash')

@app.route('/login', methods = ['POST'])
def login():

    print(request.form)

    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect("/dash")

@app.route("/users/account/<int:user_id>", methods = ['POST'])
def edit(user_id):
    data = {
        'id': user_id
    }
    user = User.get_by_id(data)
    players = Player.get_all_with_maker()
    return render_template("edit.html", user=user, players = players)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')