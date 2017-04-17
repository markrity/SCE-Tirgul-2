# -*- coding: utf-8 -*-

import os

from flask import render_template, redirect, url_for, request, g
from flask import send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from wtforms import ValidationError

from app import app, login_manager
from .models import User, Party


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def party_exists_validation(party_name):
    party = Party.query.filter_by(name=party_name).count()
    if party != 1:
        raise ValidationError("Party does not exist")
    return True


def vote_increment_by_party(party_name):



@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        party_exists_validation(request.form['party_name'])
        vote_increment_by_party(request.form['party_name'])
        return redirect(url_for('login'))
    g.user = current_user #global user parameter used by flask framwork
    parties = Party.query.all()
    return render_template('index.html',
                           title='Home',
                           user=g.user,
                           parties=parties)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':

        ## Validate user
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        id = request.form['id']
        id = int(id)
        if id!=None and id!='':
            user = User.query.filter_by(id=id).first()
            if user != None:
                if first_name != None and first_name!='':
                    if first_name==user.first_name:
                        if last_name!=None and last_name!='':
                            if last_name==user.last_name:
                                if user.Is_Voted!=True:
                                    login_user(user)  ## built in 'flask login' method that creates a user session
                                    return redirect(url_for('index'))
                                else:
                                    error=u'כבר בוצע הצבע'
                            else:
                                error = u'שפ משפחה לא תואם תז'
                        else:
                            error=u'יש להזין שם משפחה'
                    else:
                        error = u'שם פרטי לא תואם לתז'
                else:
                    error = u'יש להזין שם פרטי'
            else:
                error = u'לא קיים משתמש עם תז כזה'
        else: ##validation error
            error = u'יש להזין תז'





    return render_template('login.html',
                           error=error)


## will handle the logout request
@app.route('/logout')
@login_required
def logout():
    logout_user() ## built in 'flask login' method that deletes the user session
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
#@login_required
def handle_data():
    result = request.form
    party = request.form['party_name']
    #your code