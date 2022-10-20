import logging
from os import access

from flask import (Blueprint, Flask, redirect, render_template, request,
                   session, url_for)

from application.core.authentication import authanticate
from application.core.db.models.client_model import ClientData
from application.core.db.models.config import Config
from application.core.decorators import login_required

totp_route = Blueprint('totp_route', __name__)

@totp_route.route('/home')
@login_required
def index():
    access_token_obj = Config.query.filter_by(id=1).first()
    access_token = access_token_obj.access_token
    data = ClientData.query.all()
    return render_template('home.html', data=data, access_token=access_token)

@totp_route.route('/home/get-totp/<pk>')
@login_required
def get_totp(pk):
    access_token_obj = Config.query.filter_by(id=1).first()
    access_token = access_token_obj.access_token
    return render_template('get-totp.html', client_id=pk, access_token=access_token)

@totp_route.route('/home/update/<pk>')
@login_required
def update_totp(pk):
    access_token_obj = Config.query.filter_by(id=1).first()
    access_token = access_token_obj.access_token
    data = ClientData.query.filter_by(id=pk).first()
    return render_template('update-totp.html', id=pk, data=data, access_token=access_token)

@totp_route.route('/home/add')
@login_required
def add_totp():
    access_token_obj = Config.query.filter_by(id=1).first()
    access_token = access_token_obj.access_token         
    return render_template('add-totp.html', access_token=access_token)

@totp_route.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST': 
        email = request.form['email']
        password = request.form['password']
        auth = authanticate(email, password)
        print(auth)
        if auth:
            session['logged'] = True
            return redirect(url_for('totp_route.index'))
    return render_template('login.html')



