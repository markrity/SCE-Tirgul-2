# -*- coding: utf-8 -*-

import os

from flask import render_template, redirect, url_for, request, g
from flask import send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from wtforms import ValidationError

from app import app, login_manager
from app import db
from app.forms import LoginForm
from .models import User, Party


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def party_exists_validation(party_name):
    party = Party.query.filter_by(name=party_name).count()  # party names are unique
    if party != 1:  # if no party is found
        raise ValidationError("Party does not exist")
    return True


def vote_increment_by_party(party_name):  # update Party model vote count after user successful voting
    party = Party.query.filter_by(name=party_name).first()
    party.votes = party.votes + 1
    db.session.commit()


def update_user_voted(user_id):  # update User model 'voted' field after user successful voting
    user = User.query.filter_by(id=user_id).first()
    user.voted = True
    db.session.commit()


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        # these 3 methods should be in transaction.
        party_exists_validation(request.form['party_name'])
        vote_increment_by_party(request.form['party_name'])
        update_user_voted(current_user.id)
        logout()
        return redirect(url_for('login'))
    g.user = current_user  # global user parameter used by flask framework
    parties = Party.query.all()
    return render_template('index.html',
                           title='Home',
                           user=g.user,
                           parties=parties)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        form = LoginForm(request.form)
        ## Validate user credentials
        if form.validate():
            id_num = request.form['id_num']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            logged_user = User(int(id_num), first_name, last_name, False)
            user = User.query.filter_by(id=id_num).first()
            if None is not user:  # if the user exists check if the credentials match and that he didn't vote
                if user != logged_user:
                    error = 'Error in user credentials'
                elif user.voted:
                    error = 'User already voted'
                else:
                    login_user(user)
                    return redirect(url_for('index'))
            else:
                error = 'User doesnt exist in the system'
        else:
            error = "Invalid form"
    return render_template('login.html', error=error), 404


## will handle the logout request
@app.route('/logout')
@login_required
def logout():
    logout_user()  ## built in 'flask login' method that deletes the user session
    return redirect(url_for('index'))


## secret page that shows the user name
@app.route('/secret', methods=['GET'])
@login_required
def secret():
    return 'This is a secret page. You are logged in as {} {}'.format(current_user.first_name, current_user.last_name)


## will handle the site icon - bonus 2 points for creative new icon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route('/vote', methods=['POST'])
# @login_required
def handle_data():
    result = request.form
    party = request.form['party_name']
    # your code
