from . import app, db
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401
from bson import json_util

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

client = db.init_db()

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200


######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200


######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for i in data:
        if i["id"] == id:
            return make_response(jsonify(i), 200)
    return {"message": "picture not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.json
    if not picture:
        return {"message": "Invalid input parameter"}, 422

    for i in data:
        if picture["id"] == i["id"]:
            return {"Message": f"picture with id {picture['id']} already present"}, 302

    try:
        data.append(picture)
        return jsonify(picture), 201
    except NameError:
        return {"message": "data not defined"}, 500


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = request.json
    if not picture:
        return {"message": "Invalid input parameter"}, 422

    for index, pic in enumerate(data):
        if pic["id"] == id:
            data[index] = picture
            return picture, 201

    return {"message": "picture not found"}, 404


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for pic in data:
        if pic["id"] == id:
            data.remove(pic)
            return "", 204

    return {"message": "picture not found"}, 404


# Connecting to MongoDB from Flask
@app.route("/todos")
def index():
    result = client.tododb.todo.find({})
    return json_util.dumps(list(result)), 200


@app.route("/todos/<priority>")
def get_by_priority_better(priority):
    result = client.tododb.todo.find({"priority": priority})
    result_list = list(result)
    if not result or len(result_list) < 1:
        return json_util.dumps(result_list), 404

    return json_util.dumps(result_list), 200
