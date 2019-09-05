from fastai import *
from fastai.vision import *
from flask import Flask, jsonify, request
import os
from PIL import Image
import io


app = Flask(__name__)


@app.route('/api/classify_image/', methods=['GET', 'POST'])
def classifiy_image():
    try:
        filename = request.data["filename"]
    except:
        filename = "random.png"
    image = request.files["image"]
    img = Image.open(io.BytesIO(image.read()))
    img.save(filename)

    # Classify image
    image = open_image(filename)
    learner = load_learner('.', 'export.pkl')
    prediction = learner.predict(image)[0]
    return jsonify({'result': str(prediction)})

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)