import json
import pickle

from flask import Flask, request, json, render_template, abort

from storage import db, Map, add_to_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mars_rover.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://PaperFoldingSkil:password@PaperFoldingSkill.mysql.pythonanywhere-services.com/PaperFoldingSkil$skill"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_POOL_RECYCLE'] = 299
# app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20
db.app = app
db.init_app(app=app)
try:
    db.create_all()
except Exception as e:
    pass


@app.route("/")
def index():
    return render_template("test.html")


@app.route("/srvc/health")
def health():
    return "Service is alive"


@app.route("/srvc/map/")
def all_maps():
    maps = Map.query.all()
    maps = [pickle.loads(map_.map_data) for map_ in maps]
    return json.dumps({"maps": maps})


@app.route("/srvc/map/<int:map_id>")
def get_map(map_id):
    map_ = Map.query.filter_by(id=map_id).first()
    if not map_:
        abort(400)
    return json.dumps(pickle.loads(map_.map_data))


@app.route("/srvc/path/")
def get_path_by_map_id():
    return "ok"


@app.route("/srvc/path/map")
def get_path_by_map():
    return "ok"


@app.route("/srvc/path/cost")
def cost_by_map_id():
    return "ok"


@app.route("/srvc/path/cost_map", methods=["POST"])
def cost_by_map():
    return "ok"


@app.route("/srvc/map/upload/<int:map_id>", methods=["POST"])
def upload_map(map_id):
    json_file = request.json
    maps = Map.query.filter_by(id=map_id).all()
    if maps:
        abort(400)
        return "Alredy exist"
    new_map = Map()
    new_map.map_data = pickle.dumps(json_file)
    add_to_db(new_map)
    return "ok"


@app.route("/srvc/map/change/<int:map_id>", methods=["POST"])
def change_map(map_id):
    json_file = request.json
    map_ = Map.query.filter_by(id=map_id).first()
    if not map_:
        abort(400)
        return "Alredy exist"
    map_.map_data = pickle.dumps(json_file)
    add_to_db(map_)
    return "ok"
