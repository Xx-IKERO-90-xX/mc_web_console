import os
import sys
import json
from datetime import datetime
from flask import request, Flask, render_template, redirect, session, sessions, url_for
from werkzeug.utils import secure_filename
import asyncio
from flask_sqlalchemy import SQLAlchemy
from extensions import db
import controller.SecurityController as security
from models.User import User
from flask_socketio import SocketIO, send, emit
import multiprocessing
import controller.McServerController as mcrcon



settings = {}
with open("settings.json") as setting:
    settings = json.load(setting)

app = Flask(__name__)

app.secret_key = "a40ecfce592fd63c8fa2cda27d19e1dbc531e946"
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{settings['mysql']['user']}:{settings['mysql']['passwd']}@{settings['mysql']['host']}/{settings['mysql']['db']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.app_context()

socketio = SocketIO(app)

# Ruta principal del index
@app.route('/', methods=['GET'])
async def index():
    if 'id' in session:
        return render_template('index.jinja')
    else:
        return redirect(url_for('login'))


# Ruta para el Login
@app.route('/auth/login', methods=['GET', 'POST'])
async def login():
    if 'id' not in session:
        if request.method == 'GET':
            return render_template('login.jinja')
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
                    return render_template('login.jinja')
            else:
                error_msg = "Usuario o contraseña incorrectos!"
                return render_template('login.jinja', error_msg=error_msg)
    else:
        return redirect(url_for('index'))


# Ruta para desloguearse
@app.route('/auth/logout', methods=['GET'])
async def logout():
    session.clear()
    return redirect(url_for('index'))



## SOCKETIO
@socketio.on('send_command')
def handle_command(data):
    result_queue = multiprocessing.Queue()
    process = multiprocessing.Process(
        target=mcrcon.execute_mc_command, 
        args=(data['command'], result_queue)
    )
    
    process.start()
    process.join()

    response = result_queue.get()
    response = mcrcon.clean_output(response)

    emit('server_output', {'output': response})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    socketio.run(
        app,
        host=settings['flask']['host'],
        port=settings['flask']['port'],
        debug=settings['flask']['debug']
    )