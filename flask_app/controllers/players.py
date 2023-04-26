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
    return render_template ('dashboard.html', user = user.User.get_user_with_all_players_hes_following(data), players = player.Player.get_one_users_unfollowed_players(data))


@app.route('/players/create')
def create_player():
    if not session['user_id']:
        return redirect('/logout')
    data = {
        'user_id': session.get('user_id')
    }
    return render_template('player_create.html', user = user.User.get_by_user_id(data))


@app.route('/players/process', methods=['POST'])
def process_player():
    if not session['user_id']:
        return redirect('/logout')
    if not player.Player.validate_player(request.form):
        session['first_name'] = request.form.get('first_name')
        session['last_name'] = request.form.get('last_name')
        session['team'] = request.form.get('team')
        session['position'] = request.form.get('position')
        session['points_pg'] = request.form.get('points_pg')
        session['rebounds_pg'] = request.form.get('rebounds_pg')
        session['assists_pg'] = request.form.get('assists_pg')
        session['steals_pg'] = request.form.get('steals_pg')
        session['blocks_pg'] = request.form.get('blocks_pg')
        return redirect('/players/create')
    player_id = player.Player.save_player(request.form)
    if session.get('first_name'):
        session.pop('first_name')
    if session.get('last_name'):
        session.pop('last_name')
    if session.get('team'):
        session.pop('team')
    if session.get('position'):
        session.pop('position')
    if session.get('points_pg'):
        session.pop('points_pg')
    if session.get('rebounds_pg'):
        session.pop('rebounds_pg')
    if session.get('assists_pg'):
        session.pop('assists_pg')
    if session.get('steals_pg'):
        session.pop('steals_pg')
    if session.get('blocks_pg'):
        session.pop('blocks_pg')
    return redirect(f'/players/{player_id}')

@app.route('/players/<int:id>')
def display_player(id):
    if not session['user_id']:
        return redirect('/logout')
    player_data = {
        'id': id
    }
    user_data = {
        'user_id': session.get('user_id')
    }
    return render_template('player_view.html', player=player.Player.get_one_player_by_id(player_data), user=user.User.get_by_user_id(user_data))

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
    player_id = request.form.get('player_id')
    if not player.Player.validate_player(request.form):
        return redirect (f'/players/{player_id}/edit')
    player.Player.edit_player(request.form)
    return redirect (f'/players/{player_id}')

@app.route('/players/<int:id>/delete')
def delete_player(id):
    if not session.get('user_id'):
        return redirect('/login')
    if session.get('user_id'):
        player_data = {
            'player_id': id
        }
        returned_player = player.Player.get_one_player_with_creator(player_data)
        if session.get('user_id') != returned_player.creator.id:
            return redirect('/dashboard')
        player.Player.delete_player(player_data)
        return redirect('/dashboard')

@app.route('/players/follow/<int:id>')
def follow_player(id):
    if not session.get('user_id'):
        return redirect('/login')
    data = {
        'user_id': session.get('user_id'),
        'player_id': id
    }
    player.Player.follow_player(data)
    return redirect('/dashboard')

@app.route('/players/unfollow/<int:id>')
def unfollow_player(id):
    if not session.get('user_id'):
        return redirect('/login')
    data = {
        'user_id': session.get('user_id'),
        'player_id': id
    }
    player.Player.unfollow_player(data)
    return redirect('/dashboard')


