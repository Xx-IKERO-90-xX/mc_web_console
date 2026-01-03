import os
import sys
from flask import request, Flask, render_template, redirect, session, sessions, url_for, Blueprint
from extensions import db
import json
from models.Console import Console

console_bp = Blueprint('console', __name__)


@console_bp.route("/", methods=["GET"])
async def index(): 
    if 'id' in session:
        page = request.args.get('page', 1, type=int)
        consoles = db.session.query(Console).paginate(page=page, per_page=5)
        return render_template('console/index.jinja', consoles=consoles)
    
    return redirect(url_for('auth.login'))


