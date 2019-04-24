import os
import uuid
from urllib.request import urlopen

from flask import Flask, request, jsonify
from flask_cors import CORS

import pho2txt

app = Flask(__name__)
CORS(app)


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def check_extension(filename):
    valid_extension = ['jpg', 'jpeg', 'png']
    file_extension = filename.split('.')[-1]

    if file_extension not in valid_extension:
        raise FileNotFoundError


@app.route('/files', methods=['POST'])
def make_recognition():
    try:
        filename = str(uuid.uuid4()) + '.jpg'
        file = open(filename, 'xb+')

        if request.form.get('url'):
            file.write(urlopen(request.form.get('url')).read())
        else:
            image = request.files['image']
            check_extension(image.filename)
            image.save(dst=file)

        file.close()

        recognizer = pho2txt.PhotoToTxt(filename)
        rects, confidence = recognizer.text_detection()
        text = recognizer.text_recognition(rects)

        os.remove(filename)

        return jsonify(text)

    except FileNotFoundError:
        response = jsonify({"message": "Server does not recognize files with this extension!"})
        response.status_code = 501
        return response

    except Exception as e:
        response = jsonify({"message": str(e)})
        response.status_code = 500
        return response


if __name__ == '__main__':
    app.run()
