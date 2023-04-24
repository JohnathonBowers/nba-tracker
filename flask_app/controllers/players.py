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

@app.route('/players/<int:id>/edit')
def display_edit_player_form(id):
    if not session.get('user_id'):
        return redirect('/login')
    if session.get('user_id'):
        player_data = {
            'player_id': id
        }
        user_data = {
            'user_id': session.get('user_id')
        }
        returned_player = player.Player.get_one_player_with_creator(player_data)
        if session.get('user_id') != returned_player.creator.id:
            return redirect('/dashboard')
        return render_template('player_edit.html', player = player.Player.get_one_player_with_creator(player_data), user = user.User.get_by_user_id(user_data))
    
@app.route('/players/edit-submit', methods=['POST'])
def edit_player():
    if not player.Player.validate_player(request.form):
        player_id = request.form.get('player_id')
        return redirect (f'/players/{player_id}/edit')
    player.Player.edit_player(request.form)
    return redirect ('/dashboard')

