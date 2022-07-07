from flask import Flask

app = Flask(__name__)

from app import routes
from app import models
from flask_cors import CORS

CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:12345@localhost:5432/covid-stats"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

