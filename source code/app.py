from flask import Flask, request, jsonify
from flask_cors import CORS
import pho2txt
import os

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


@app.route('/files', methods=['POST'])
def make_recognition():
    try:
        image = request.files['image']

        file = open(image.filename, 'rb+')
        image.save(dst=file)
        file.close()

        text = pho2txt.to_txt(image.filename, 'ta')
        os.remove(image.filename)

        return jsonify(text)
    
    except Exception:
        response = jsonify({"message": "Internal server error"})
        response.status_code = 500
        return response


if __name__ == '__main__':
    app.run()
