from app import models
from app import utils
import cv2
import imutils
import numpy
import pytesseract
import time


def contains_licence_plates(licence_plates, date):
    # noinspection PyUnresolvedReferences
    stored_licence_plates = models.LicencePlate.query.filter(
        models.LicencePlate.time >= date
    ).all()
    resp = []
    for licence_plate in licence_plates:
        plate = next((x for x in stored_licence_plates if x.plate == licence_plate), None)
        # Add date check
        resp.append({
            "plate": licence_plate,
            "detected": plate is not None,
            "time": utils.convert_timestamp_to_iso(plate.time) if plate is not None else ""
        })

    return resp


def parse_image(image):
    models.database.db.create_all()
    if image is None:
        return None

    image = cv2.imdecode(numpy.fromstring(image, numpy.uint8), cv2.IMREAD_UNCHANGED)
    image = cv2.resize(image, (640, 480))  # reduce image size

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # remove colors
    gray = cv2.bilateralFilter(gray, 13, 15, 15)  # blur image to remove noise

    # find image contours
    edges = cv2.Canny(gray, 30, 200)  # detect image edges
    contours = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    plate = None
    for contour in contours:
        # approximate the contour
        approx = cv2.approxPolyDP(contour, 0.018 * cv2.arcLength(contour, True), True)
        # if our approximated contour has four points, then we can assume that it is plate
        if len(approx) == 4:
            plate = approx
            break

    if plate is None:
        return None

    # Masking the part other than the number plate
    mask = numpy.zeros(gray.shape, numpy.uint8)
    cv2.drawContours(mask, [plate], 0, 255, -1, )
    cv2.bitwise_and(image, image, mask=mask)

    # Now crop
    (x, y) = numpy.where(mask == 255)
    (top_x, top_y) = (numpy.min(x), numpy.min(y))
    (bottom_x, bottom_y) = (numpy.max(x), numpy.max(y))
    cropped = gray[top_x:bottom_x + 1, top_y:bottom_y + 1]

    # Read the number plate
    config = utils.get_tesseract_config(pytesseract)
    text = pytesseract.image_to_string(cropped, config=config)

    # remove new lines and remove '-' character
    return text.partition("\n")[0].replace('-', '')


def save_licence_plate(plate):
    licence_plate = models.LicencePlate(plate=plate, time=int(time.time()))
    licence_plate.save()
