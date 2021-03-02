from app import app
from flask import jsonify, request
from app import services
from app import utils


def error_response(message):
    return jsonify({
        "message": message
    }), 400


@app.route("/upload-camera-image", methods=["POST"])
def upload_camera_image():
    if not request.files:
        return error_response("Image file is missing")

    if "image" not in request.files:
        return error_response("Attribute name of image should be named 'image'")

    image = request.files["image"]

    if image.mimetype not in ["image/png", "image/jpg", "image/jpeg"]:
        return error_response("Allowed image files are in PNG or JPG format")

    plate = services.parse_image(image.read())
    if plate is None:
        return jsonify({"message": "No licence plate found", "status": 404})
    else:
        services.save_licence_plate(plate)
        return jsonify({"message": f"Licence plate '{plate}' found", "status": 200})


@app.route("/check-licence-plate/<licence_plates>/<date>", methods=["GET"])
def upload_image(licence_plates, date):
    licence_plates = licence_plates.split(',')
    date = utils.convert_iso_to_timestamp(date)
    return jsonify(services.contains_licence_plates(licence_plates, date))
