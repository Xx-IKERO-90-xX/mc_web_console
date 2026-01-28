import os
import sys
from flask import request, Flask, flash, render_template, redirect, session, sessions, url_for, Blueprint
from extensions import db
import json
from models.Console import Console
import controller.SecurityController as security
import controller.McServerController as mcrcon

console_bp = Blueprint('console', __name__)

@console_bp.route("/", methods=["GET"])
async def index(): 
    if 'id' in session:
        page = request.args.get('page', 1, type=int)
        consoles = db.session.query(Console)
        
        for console in consoles:
            if await mcrcon.test_connection(console.ip, console.port):
                console.status = "online"

        consoles = consoles.paginate(page=page, per_page=5)
        return render_template('console/index.jinja', consoles=consoles)
    
    return redirect(url_for('auth.login'))

@console_bp.route("/add", methods=["POST"])
async def add_console():
    if 'id' in session:
        name = request.form.get('name')
        ip = request.form.get('ip')
        passwd = request.form.get('passwd')
        passwd2 = request.form.get('passwd2')
        port = 0

        try:
            port = int(request.form.get('port'))
        except ValueError:
            flash("Hay fallos en los datos ingresados!", "error")
            return redirect(url_for('console.index'))
        
        if passwd != passwd2:
            flash("Las contraseñas no coinciden!", "error")
            return redirect(url_for('console.index'))
        
        passwd_hashed = await security.encrypt_passwd(passwd)
        
        try:
            new_console = Console(name=name, ip=ip, port=port, passwd=passwd_hashed ,status="Offline")
            db.session.add(new_console)
            db.session.commit()
        except Exception as e:
            flash("Error al agregar la consola! Verifique que el nombre o IP no estén repetidos.", "error")
            return redirect(url_for('console.index'))
        
        return redirect(url_for('console.index'))

    return redirect(url_for('auth.login'))

@console_bp.route("/delete/<int:id>", methods=["GET"])
async def delete_console(id):
    if 'id' in session:
        console = db.session.query(Console).filter(Console.id == id).first()

        if console:
            db.session.delete(console)
            db.session.commit()

            return redirect(url_for('console.index'))

        flash("Consola no encontrada!", "error")
        return redirect(url_for('console.index'))

    return redirect(url_for('auth.login'))