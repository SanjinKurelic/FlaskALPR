# Flask ALPR

Flask ALPR is a web service for automatic license plate recognition (ALPR). ALPR is a technology that uses optical character recognition on images to read vehicle registration plates. It is used by police forces, for electronic toll collection on pay-per-use roads and as a method of cataloguing the movements of traffic.

The web service is written in Python using Flask for REST API and OpenCV with PyTesseract for plate recognition. The service offers two REST API-s, one for checking if licence plate is detected and one for detecting licence plate from camera image. All detected licence plates are automatically stored in a SQLite database using the SQLAlchemy library.

## Getting started

### Requirements

To start the web service you should have **Python 3.8 or higher** and **Tesseract-OCR** program installed. Tesseract-OCR program is available on all platforms and can be installed using 
official documentation: https://github.com/tesseract-ocr/tesseract. For Windows you can install program in `C:/Program Files/Tesseract-OCR/tesseract.exe` path so it's compatible with current code without the extra configuration. Linux will work out-of-the-box.

To install required Python modules using PIP, you can use the following command in the project root directory:

```bash
pip3 install -r requirements.txt
```

### Running

It's recommended to set Python virtual environment before running script or to use PyCharm program which will do this automatically. To start the web service run the following command:

```bash
python3 run.py
```

## REST API

There are two available API-s defined in the web service - one for detecting licence plates from the image, and the other for checking if given licence plate is detected.

### Detecting licence plate from image

Web service can detect licence plate from all cameras that have the ability to save images in JPG or PNG format. Testing the service could also be done using Postman or a similar program with example images from the Internet. Images like this one below will work without any problems and licence plate will be extracted from the image (licence plate on given image is blurred because this is a live image captured from the security camera).

<p align="center"><img src="https://github.com/SanjinKurelic/FlaskALPR/blob/master/media/licencePlate.jpg" alt="Licence plate example image"/></p>

#### Request

```
POST /upload-camera-image

Content-Type: multipart/form-data
Content-Disposition: form-data; name="image"; filename="<file.jpg>"
Content-Type: image/jpeg
```

#### Repsponse

If licence plate is detected:

Status code - 200 OK

```json
{
  "message": "Licence plate AB1234CD found",
  "status": 200
}
```

If licence plate is not detected:

Status code - 200 OK

```json
{
  "message": "No licence plate found",
  "status": 404
}
```

### Checking if licence plate is detected

For checking if given licence plate is detected from last time check was made `GET` request can be sent to `check-licence-plate` URL with two variables: 

- licence plate or comma separated licence plates that we need to check, for example: `AB1234AB`, or `AB1234AB,CD567EF,GH888II`
- ISO datetime from the last check, for example: `2020-12-01T19:15:00`
  
The service will check if licence plate is detected in the interval from given datetime and current datetime. If licence plate is detected the time of detection will be filled.

#### Request

```
GET /check-licence-plate/<licence plate>/<iso datetime>
```

#### Response

If licence plates are detected:

Status code - 200 OK

```json
[
  {
    "detected": true,
    "plate": "AB1234AB",
    "time": "2020-12-01T19:14:23"
  }
]
```

If licence plates are not detected:

Status code - 200 OK

```json
[
  {
    "detected": false,
    "plate": "AB1234AB",
    "time": ""
  }
]
```

## Technologies

- Flask
- SQLAlchemy
- python-dateutil
- opencv-python-headless
- imutils
- numpy
- pytesseract
