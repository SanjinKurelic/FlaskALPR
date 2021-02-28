from app import app
from flask import jsonify, request


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

    # TODO add OCR logic here
    return jsonify({"message": "Image was successfully stored"})


# TODO use database instead of hardcoded value
sk_lp = {
    "RI1234AB": "2020-12-01T22:45:37"
}


@app.route("/check-licence-plate/<licence_plates>/<date>", methods=["GET"])
def upload_image(licence_plates, date):
    resp = []
    for licence_plate in licence_plates.split(","):
        # TODO Fetch data rom database for given date and licence plate
        resp.append({
            "plate": licence_plate,
            "detected": licence_plate in sk_lp,
            "time": sk_lp[licence_plate] if licence_plate in sk_lp else ""
        })

    return jsonify(resp)
