from flask import Flask, request
from flask_cors import CORS
import pho2txt
import scipy.misc
import os

app = Flask(__name__)
CORS(app)


@app.route('/files', methods=['POST'])
def make_recognition():
    image = request.files['image']

    file = open(image.filename, 'rb+')
    image.save(dst=file)
    file.close()

    output = pho2txt.binarization(image.filename, 'ta')
    scipy.misc.imsave('output.jpg', output)
    os.remove(image.filename)

    return image.filename


if __name__ == '__main__':
    app.run()
