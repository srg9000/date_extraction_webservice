import os
from flask import Flask, render_template, request, Response
from io import BytesIO
import base64
import numpy as np
import tempfile
import jsonpickle

# import our OCR function
from task_receipt import extract_date
pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
# define a folder to store and later serve the images
UPLOAD_FOLDER = '/static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

# function to check the file extension


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# route and function to handle the home page


@app.route('/')
def home_page():
    return render_template('index.html')

# route and function to handle the upload page


@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if there is a file in the request
        req_data = request.get_json()
        img_data = req_data['base_64_image_content']

        with open("imageToSave.png", "wb") as fh:
            fh.write(base64.decodebytes(img_data))
        fh.close()
        # call the OCR function on it
        extracted_text = extract_date("imageToSave.png")

        # extract the text and display it
        response = {'date': extracted_text}
        # encode response using jsonpickle
        response_pickled = jsonpickle.encode(response)

        return Response(response=response_pickled, status=200, mimetype="application/json")
    else:
	    return Response(response=jsonpickle.encode({'date': None}), status=200, mimetype="application/json")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
