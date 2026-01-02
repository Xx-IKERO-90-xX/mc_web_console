import os
import sys
from flask import request, Flask, render_template, redirect, session, sessions, url_for, Blueprint
from extensions import db
import json

console_bp = Blueprint('console', __name__)


@console_bp.route("/", methods=["GET"])
async def index(): 
    if 'id' in session:
        return render_template('console/index.jinja')
    
    return redirect(url_for('auth.login'))


