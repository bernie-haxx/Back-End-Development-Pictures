from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# DATA FUNCTIONS
######################################################################


def find_pic(id):
    pic_id_dict = [pic["id"] for pic in data]

    # Check the id is in the dict
    if id in pic_id_dict:
        return [pic for pic in data if pic["id"] == id ][0]


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
    """
    Return pictures from the data list
    """
    app.logger.info("Requesting for list of pictures")

    if data:
        app.logger.info(f"Pictures found in total: {len(data)}")

        # return the data in json with 200 status
        return jsonify(data), 200
    
    # return 500 if data is not found
    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """
    Return picture via id in data list
    """
    app.logger.info(f"Requesting Picture with id: {id}")
    
    if data:
        picture = find_pic(id)
        if picture:
            app.logger.info(f"Picture Found with id: {id}")
            return jsonify(picture), 200
        else:
            return {"message": "Not Found"}, 404
    
    return {"message": "Internal server error"}, 500
        

######################################################################
# CREATE A PICTURE
######################################################################


@app.route("/picture", methods=["POST"])
def create_picture():
    if data:
        app.logger.info("Requesting for Picture Creation")
        picture = request.json

        if picture:
            existing_pic = find_pic(picture['id'])
            if existing_pic:
                app.logger.info(f"picture with id {picture['id']} already present")
                return {"Message": f"picture with id {picture['id']} already present"}, 302

            data.append(picture)
            app.logger.info(f"Creation Success: Picture with id {picture['id']}")
            return jsonify(picture), 201
    
    return {"message": "Internal server error"}, 500
    


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    app.logger.info(f"Requesting for Update on Picture with id: {id} ")
    pic_req = request.json
    picture = find_pic(id)
    
    if picture:
        app.logger.info("Updating sequence...")
        picture.update(pic_req)

        return jsonify(picture), 204
    
    else:
        return {"message": "Not Found"} , 404
    
    return {"message": "Internal server error"}, 500


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    # app.logger.info(f"Requesting for Deletion on Picture with id: {id} ")
    picture = find_pic(id)

    if picture:
        # app.logger.info(f"Picture found with id: {picture['id']} ")

        data.remove(picture)
        # app.logger.info("Deletion Sequence...")
        return {}, 204
    
    return {"message": "picture not found"}, 404
