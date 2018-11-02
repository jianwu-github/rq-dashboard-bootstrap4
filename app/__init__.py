import os
import logging

from flask import Flask
from config import Config

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.from_object(Config)

from app import routes
