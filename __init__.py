# -*- coding: UTF-8 -*-

from flask import Flask
app = Flask(__name__)

from bitam import app

# Run Bitam (Flask) app
app.run()
