from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Databas-konfiguration (använd SQLite eller PostgreSQL)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resonate.db'  # För SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
