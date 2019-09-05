from flask import Flask, jsonify, request
from step_to_image import classify_step

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
        classifications = classify_step(filename)
        # print("hiya")
    except:
        return jsonify("Failed to classify STEP")

    return jsonify(classifications)


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)