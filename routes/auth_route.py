import os
import sys
from flask import request, Flask, render_template, redirect, session, sessions, url_for, Blueprint
from extensions import db
import json
from models.User import User
import controller.SecurityController as security

auth_bp = Blueprint('auth', __name__)

# Ruta para el Login
@auth_bp.route('/login', methods=['GET', 'POST'])
async def login():
    if 'id' not in session:
        if request.method == 'GET':
            return render_template('auth/login.jinja')
        else:
            username = request.form.get('username')
            passwd = request.form.get('passwd')

            if await security.verify_login(username, passwd):
                user = db.session.query(User).filter(User.username == username).first()
                if user.mc_console or user.role == 'Admin':
                    session['id'] = user.id
                    session['username'] = user.username
                    return redirect(url_for('index'))
                else:
                    error_msg = "Acceso no autorizado!"
                    return render_template('auth/login.jinja')
            else:
                error_msg = "Usuario o contraseña incorrectos!"
                return render_template('auth/login.jinja', error_msg=error_msg)
            
    return redirect(url_for('index'))

# Ruta para desloguearse
@auth_bp.route('/logout', methods=['GET'])
async def logout():
    session.clear()
    return redirect(url_for('index'))