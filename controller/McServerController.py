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


# Permite la ejecución de un comando del servidor de minecraft a través de la aplicación web
def execute_mc_command(command, ip, port, passwd, result_queue):
    response = ""
    
    with MCRcon(ip, passwd, port=port) as mcr:
        response = mcr.command(command)
        result_queue.put(response)

async def test_connection(ip, port, passwd):
    try:
        with MCRcon(ip, passwd, port=port) as mcr:
            response = mcr.command("list")
            return True
    except Exception as e:
        return False
    

# Corrige ciertas imperfecciones en la salida de los comandos
def clean_output(output):
    return re.sub(r"§.", "", output)