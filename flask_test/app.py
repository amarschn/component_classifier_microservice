from flask import Flask, request, render_template, session, send_file
from forms import StepUploadForm
import requests
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
import os
import shutil
from uuid import uuid4


app = Flask(__name__)
csrf = CSRFProtect(app)
csrf.init_app(app)
app.config['SECRET_KEY'] = 'hi'
app.config['ALLOWED_EXTENSIONS'] = ['STEP', 'step']
app.config['UPLOADED_STEP_FILES_DEST'] = os.getcwd() + '/step_uploads'
# app.config['COMPONENT_CLASSIFIER_URL'] = 'http://68.183.158.9:5000/api/classify_step/'
app.config['COMPONENT_CLASSIFIER_URL'] = 'http://component_classifier_cq_1:5000/api/classify_step/'


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
        if not os.path.exists(app.config['UPLOADED_STEP_FILES_DEST']):
            os.mkdir(app.config['UPLOADED_STEP_FILES_DEST'])
        step.filename = os.path.join(app.config['UPLOADED_STEP_FILES_DEST'], step_filename)


        if allowed_file(step.filename, 'step'):
            step.save(step.filename)
            files = {'step': open(step.filename, 'rb')}
            payload = {'filename': 'hello.step'}
            r = requests.post(app.config['COMPONENT_CLASSIFIER_URL'], files=files, data=payload, stream=True)

            img_id = str(uuid4())
            session['img_id'] = img_id
            image = 'static/{}.png'.format(img_id)
            
            with open(image, 'wb') as img:
                img.write(r.content)
        else:
            flash('Invalid file type! Only STEP files can be uploaded.')
        
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


@app.route("/cc_image")
def cc_image():
    img_id = session['img_id']
    return send_file(os.path.join(app.root_path,'static/{}.png'.format(img_id)), cache_timeout=0)


def allowed_file(filename, file_type):
    """Determines whether filename has acceptable extension
    """
    extension = filename.rsplit('.', 1)[1].lower()
    if ('.' in filename) and \
       (extension in app.config['ALLOWED_EXTENSIONS']) and \
       (extension == file_type):
        return True
    else:
        return False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)