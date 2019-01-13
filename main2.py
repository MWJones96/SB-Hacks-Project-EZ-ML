# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_flex_quickstart]

import logging
import os
import hashlib
from multiprocessing import JoinableQueue, Process


from flask import allowed_file, Flask, flash, request, render_template, redirect, secure_filename
from flask_mail import Mail,Message

from urllib.parse import urljoin
# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

from constants import SID,TOKEN

from ML import models
import google.storage
import LOCATION_ID

app = Flask(__name__)
mail = Mail(app)
Q = JoinableQueue(4) 

app.config['UPLOAD_FOLDER'] = 'https://storage.googleapis.com/sbhacksv-temp'

CLOUD_STORAGE_BUCKET = 'https://storage.googleapis.com/sbhacksv-temp'


@app.route('/')
def index():
    """Return a friendly HTTP greeting."""
    return render_template('index.html')

@app.endpoint('static')
def static(filename):
    static_url = app.config.get('STATIC_URL')
    if static_url:
        return redirect(urljoin(static_url, filename))
    return app.send_static_file(filename)

@app.route('/req',methods=['POST'])
def req():
    save_files(request,['train-data','train-targets','test-data'])
    modelType = request.args.get('selection', '')
    if modelType in ["neural-net","knn","svm","rf", "dt"]:

        p = Process(target=trainer,args=(request.args,))
        Q.put(p)
        Q.get_nowait()
        return render_template("success.html")
    else:
        return render_template("failure.html")


def save_files(req, names):
    # Create a Cloud Storage client.
    gcs = storage.Client()

    email = req.args.get("email")

    edigest = hashlib.sha256().update(email).hexdigest()

    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

    uploaded_file = req.files['train-data']
    
    # Create a new blob and upload the file's content.
    blob = bucket.blob(edigest + 'train-data')
    blob.upload_from_string(
        uploaded_file.read(),
        content_type=uploaded_file.content_type
    )

    uploaded_file = req.files['test-targets']
    #  Create a new blob and upload the file's content.
    blob = bucket.blob(edigest + 'train-data');
    blob.upload_from_string(
        uploaded_file.read(),
        content_type=uploaded_file.content_type
    )
    

    uploaded_file = req.files['test-data']
    #  Create a new blob and upload the file's content.
    blob = bucket.blob(edigest+'test-data');

    blob.upload_from_string(
        uploaded_file.read(),
        content_type=uploaded_file.content_type
    )


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500




# Your Account Sid and Auth Token from twilio.com/console
account_sid = SID
auth_token = TOKEN
client = Client(account_sid, auth_token)


def trainer(args):
    modelType = args.get('selection', '')    
    if modelType in ["nn","knn","svm","rf", "dt"]:
        msg = Message("Finished Learning", sender="admin@ezmlmodel.com",
                recipients=[args.get("email","eye942@gmail.com")])
        models.run_model(modelType, **args)
        mail.send(msg)
        message = client.messages \
                .create(
                     body="Your model has finished... melting... 😆😆",
                     from_='+14803729727',
                     to=args.get("phone",'+14803729727')
                 )
    


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_flex_quickstart]
