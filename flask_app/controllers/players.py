from flask_app import app
from flask import render_template, redirect, request, session
from flask_bcrypt import Bcrypt 

from flask_app.models import user, player

bcrypt = Bcrypt(app)

@app.route('/dashboard')
def dashboard():
    if not session.get('user_id'):
        session.clear()
        return redirect('/login')
    data = {
        'user_id': session.get('user_id')
    }

    players = player.Player.get_all_players()

    return render_template ('dashboard.html', user = user.User.get_by_user_id(data), players=players)


@app.route('/players/create')
def create_player():
    if not session['user_id']:
        return redirect('/logout')
    return render_template('player_create.html')


@app.route('/players/process', methods=['POST'])
def process_player():
    if not session['user_id']:
        return redirect('/logout')
    
    if not player.Player.validate_player(request.form):
        return redirect('/players/create')
    
    player.Player.save_player(request.form)
    return redirect('/dashboard')

@app.route('/players/<int:id>')
def display_player(id):
    if not session['user_id']:
        return redirect('/logout')
    data = {
        'id': id
    }
    return render_template('player_view.html', player=player.Player.get_one_player_by_id(data))


# @app.route('/create_link')
# def new_player():
#     if 'user_id' not in session:
#         return redirect('/')
#     return render_template('create_player.html')


# @app.route('/create', methods=["POST"])
# def new_players():
#     if 'user_id' not in session:
#         return redirect('/')
#     if not Player.validate_player(request.form):
#         return redirect('/create_link')
#     print(request.form)
#     data = {
#         "playername": request.form["playername"],
#         "playerteam" : request.form["playerteam"],
#         "playerposition": request.form["playerposition"],
#         "playerppg" : request.form["playerppg"],
#         "playerrpg": request.form["playerrpg"],
#         "playerapg" : request.form["playerapg"],
#         "playerspg": request.form["playerspg"],
#         "playerbpg" : request.form["playerbpg"],
#         'users_id': session['user_id']
#     }
    
#     Player.create_a_player(data)
    
#     return redirect('/dash')

# @app.route('/dash')
# def i_have_been_made():
#     if 'user_id' not in session:
#         return redirect('/')
#     data = {
#         'id': session['user_id']
#     }
#     players = Player.get_all_with_maker()


#     return render_template('dashboard.html', current_user = User.get_by_id(data),  players=players)

# @app.route("/view_player/<int:player_id>")
# def show_me_da_playerss(player_id):
#     if 'user_id' not in session:
#         return redirect('/')
#     data = {
#         'id': session['user_id']
#     }
#     player_data = {
#         'id' : player_id
#     }
#     current_player = Player.get_player_by_id(player_data)

#     return render_template('view_player.html', current_user = User.get_by_id(data), current_player=current_player)

# @app.route("/view_player/<int:player_id>")
# def edit_player(player_id):
#     data = {
#         'id': player_id
#     }
#     players = Player.get_all_with_maker()
#     return render_template("edit.html", players = players)

# @app.route('/view_player/edit/<int:player_id>', methods=['POST'])
# def update_player(player_id):
#     if not Player.validate_player(request.form):
#         return redirect(f"/view_player/edit/{player_id}")
#     data = {
#         'id': player_id,
#         "playername": request.form["playername"],
#         "playerteam" : request.form["playerteam"],
#         "playerposition": request.form["playerposition"],
#         "playerppg" : request.form["playerppg"],
#         "playerrpg": request.form["playerrpg"],
#         "playerapg" : request.form["playerapg"],
#         "playerspg": request.form["playerspg"],
#         "playerbpg" : request.form["playerbpg"],
#     }
#     Player.update(data)
#     return redirect("/dash")

