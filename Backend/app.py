import json

from flask import Flask, request, json, render_template

# from db import db

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///origami.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://PaperFoldingSkil:password@PaperFoldingSkill.mysql.pythonanywhere-services.com/PaperFoldingSkil$skill"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_POOL_RECYCLE'] = 299
# app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20
# db.app = app
# db.init_app(app=app)
# try:
#     db.create_all()
# except Exception as e:
#     pass


@app.route("/")
def index():
    return render_template("test.html")


@app.route("/srvc/health")
def health():
    return "Service is alive"


@app.route("/srvc/map/")
def all_maps():
    return "all maps"


@app.route("/srvc/map/<int:map_id>")
def get_map(map_id):
    return json.dumps({"map_id": map_id})


@app.route("/srvc/path/")
def get_path_by_map_id():
    return "ok"


@app.route("/srvc/path/map")
def get_path_by_map():
    return "ok"


@app.route("/srvc/path/cost")
def cost_by_map_id():
    return "ok"


@app.route("/srvc/path/cost_map")
def cost_by_map():
    return "ok"


@app.route("/srvc/map/upload")
def upload_map():
    return "ok"
