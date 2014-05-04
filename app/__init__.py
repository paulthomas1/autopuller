# !/usr/bin/env python
import io
import os
import re
import sys
import json
import subprocess
import requests
import ipaddress
from flask import Flask, request, abort

app = Flask(__name__)
# Giant hack to store git post data. Global state FTW
app.config['repo_data'] = "none"
repo_meta = "none"

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return ' Nothing to see here, move along {}'.format(app.config['fish'])

    elif request.method == 'POST':
        if request.headers.get('X-GitHub-Event') == "ping":
            return json.dumps({'msg': 'Hi!'})
        if request.headers.get('X-GitHub-Event') != "push":
            return json.dumps({'msg': "wrong event type"})

        payload = json.loads(request.data)
        repo_meta = {
            'name': payload['repository']['name'],
            'owner': payload['repository']['owner']['name'],
        }
        print(repo_meta)
        app.config['repo_data'] = repo_meta
        return 'OK'
