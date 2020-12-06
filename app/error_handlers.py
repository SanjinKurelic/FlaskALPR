from app import app
from flask import jsonify


@app.errorhandler(Exception)
def error_handler(e):
    return jsonify({
        "message": str(e)
    }), e.code if e.code else 500
