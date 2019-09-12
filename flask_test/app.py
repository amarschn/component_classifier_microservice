from flask import Flask, request, render_template
from forms import StepUploadForm
import requests
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
import os

CLASSIFIER_URL = 'http://localhost:5000/api/classify_step/'

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
    if form.validate_on_submit():
        step = request.files['step_file']
        step_filename = secure_filename(step.filename).replace(' ','_')
        step.filename = os.path.join('.',step_filename)
        step.save(step.filename)
        files = {'step': open(step.filename, 'rb')}
        payload = {'filename': 'hello.step'}
        r = requests.post(CLASSIFIER_URL, files=files, data=payload)
    return render_template('upload_step.html', title='Home',form=form)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)