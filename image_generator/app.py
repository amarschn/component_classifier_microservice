from flask import Flask, jsonify, request, send_file
from step_to_image import classification_image

app = Flask(__name__)


# Upload a step, and get back a classification summary
@app.route('/api/classify_step/', methods=['POST'])
def step_classification():
    try:
        filename = request.data["filename"]
    except:
        filename = "random.STEP"

    step = request.files["step"]
    try:
        step.save(filename)
    except:
        return jsonify("Failed to save STEP")

    try:
        f = classification_image(filename)
        # classifications = classify_step(filename)
        # print(type(classifications))
    except:
        return jsonify("Failed to classify STEP")

    return send_file(f, cache_timeout=0, mimetype='image/png')

if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)