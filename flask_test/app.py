from flask import Flask, request, render_template
from forms import StepUploadForm
import requests
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
import os
import shutil

CLASSIFIER_URL = 'http://component_classifier_cq_1:5000/api/classify_step/'

app = Flask(__name__)
csrf = CSRFProtect(app)
csrf.init_app(app)
app.config['SECRET_KEY'] = 'hi'

@app.route("/")
def hello():
    return "Hello Fat World!"

@app.route("/upload_step", methods=['GET', 'POST'])
def classify_step():
    form = StepUploadForm()
    image = None
    if form.validate_on_submit():
        step = request.files['step_file']
        step_filename = secure_filename(step.filename).replace(' ','_')
        step.filename = os.path.join('.',step_filename)
        step.save(step.filename)
        files = {'step': open(step.filename, 'rb')}
        payload = {'filename': 'hello.step'}
        r = requests.post(CLASSIFIER_URL, files=files, data=payload, stream=True)
        # print(r.content)
        image = 'static/classification.png'
        with open(image, 'wb') as img:
            img.write(r.content)
        

    return render_template('upload_step.html', title='Home',form=form, image=image)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)