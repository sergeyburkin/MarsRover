import os
import pickle
from datetime import datetime
from time import time

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


DAY_FOR_RESET = 2


class Map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    map_data = db.Column(db.PickleType)
