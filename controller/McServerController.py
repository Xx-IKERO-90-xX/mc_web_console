import os 
import sys
from flask import request, Flask, render_template, redirect, session, sessions, url_for
import json
import random
import asyncio
from mcrcon import MCRcon
import multiprocessing
import re

sys.path.append("..")

app_route = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
if app_route not in sys.path:
    sys.path.insert(0, app_route)

import app

settings = {}
with open('settings.json') as archivo:
    settings = json.load(archivo)

HOST = settings["mcrcon"]["host"]
RCON_PORT = settings["mcrcon"]["port"]
PASSWD_RCON = settings["mcrcon"]["passwd"]


# Permite la ejecución de un comando del servidor de minecraft a través de la aplicación web
def execute_mc_command(command, result_queue):
    response = ""
    
    with MCRcon(HOST, PASSWD_RCON, port=RCON_PORT) as mcr:
        response = mcr.command(command)
        result_queue.put(response)

# Corrige ciertas imperfecciones en la salida de los comandos
def clean_output(output):
    return re.sub(r"§.", "", output)