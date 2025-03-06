from dotenv import load_dotenv
from pprint import pprint
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import requests
import os

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return "Hello World!"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)