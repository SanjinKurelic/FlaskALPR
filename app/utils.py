from dateutil import parser
from datetime import datetime
import time
import os


def convert_iso_to_timestamp(date):
    return int(time.mktime(parser.isoparse(date).timetuple()))


def convert_timestamp_to_iso(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%S')


# noinspection SpellCheckingInspection
def get_tesseract_config(pytesseract):
    # for Linux it's usually available trough environment path
    if os.name == 'nt':
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # we could also use user-pattern like \A\A \d\d\d-\A\A
    config = '--psm 11 -c tessedit_char_whitelist=123456789ABCDEFGHIJKLMNOPRSTUVZ-'
    return config
