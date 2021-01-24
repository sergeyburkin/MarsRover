import json
import pickle
import time

from flask import Flask, request, json, render_template, abort

from storage import db, Map, add_to_db
from algo import json_data_with_path, get_cost_from_json, save_map_image_with_path

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


@app.route("/srvc/path", methods=["POST"])
def get_path_by_map_id():
    data = request.json
    if all([data.get("id"), data.get("start"), data.get("finish")]):
        start = data.get("start")
        finish = data.get("finish")
        map_ = Map.query.filter_by(id=data.get("id")).first()
        if not map_:
            abort(404)
        map_ = pickle.loads(map_.map_data)
        map_["start"] = start
        map_["finish"] = finish
        return json.dumps(json_data_with_path(map_))
    abort(400)


@app.route("/srvc/path/map", methods=["POST"])
def get_path_by_map():
    data = request.json
    return json.dumps(json_data_with_path(data))


@app.route("/srvc/path/map/img", methods=["POST"])
def get_path_by_map_img():
    data = request.json
    filename = "static/{}.png".format(int(time.time()))
    success = save_map_image_with_path(json_data_with_path(data), filename) is None
    print(success)
    return json.dumps({"success_saving": success, "img_filename": filename})


@app.route("/srvc/path/cost")
def cost_by_map_id():
    data = request.json
    if all([data.get("id"), data.get("start"), data.get("finish"), data.get("path")]):
        start = data.get("start")
        finish = data.get("finish")
        map_ = Map.query.filter_by(id=data.get("id")).first()
        if not map_:
            abort(404)
        map_ = pickle.loads(map_.map_data)
        map_["start"] = start
        map_["finish"] = finish
        map_["path"] = data.get("path")
        days, remaining_energy, spent_energy = get_cost_from_json(map_)
        return json.dumps({"days": days, "remaining_energy": remaining_energy, "spent_energy": spent_energy})
    abort(400)


@app.route("/srvc/path/cost_map", methods=["POST"])
def cost_by_map():
    data = request.json
    if not data.get("path"):
        data = json_data_with_path(data)
    days, remaining_energy, spent_energy = get_cost_from_json(data)
    return json.dumps({"days": days, "remaining_energy": remaining_energy, "spent_energy": spent_energy})


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
