import os
import json
import docx2txt

from gensim.summarization import summarize
from werkzeug.utils import secure_filename
from flask import request,flash,url_for,redirect

ALLOWED_EXTENSIONS = set(['docx'])
UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))+"/uploads"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def uplaod_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return 'not ok'
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return 'not ok'

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        user_path = os.path.join(UPLOAD_FOLDER, filename)

    file.save(user_path)
    return summarize_file(user_path)

def summarize_file(user_path):
    _no_summarized = docx2txt.process(user_path)
    _summarized = summarize(_no_summarized)

    result = {
        "no_summarized" :_no_summarized,
        "summarized": _summarized
    }

    return json.dumps(result)
