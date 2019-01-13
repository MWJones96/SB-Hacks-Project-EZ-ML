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

from flask import allowed_file, Flask, flash, request, render_template, redirect, secure_filename
from urllib.parse import urljoin
from ML import models
import google.storage
import LOCATION_ID
from google.cloud import tasks_v2beta3
from google.protobuf import timestamp_pb2

QUEUE_ID='my-appengine-queue'

app = Flask(__name__)


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

        # Create a client.
        client = tasks_v2beta3.CloudTasksClient()

        # TODO(developer): Uncomment these lines and replace with your values.
        project = 'ML Server'
        queue = 'my-appengine-queue'
        location = 'us-west2'
        payload = request.args

        # Construct the fully qualified queue name.
        parent = client.queue_path(project, location, queue)

        # Construct the request body.
        task = {
                'app_engine_http_request': {  # Specify the type of request.
                    'http_method': 'POST',
                    'relative_uri': '/train_handler'
                }
        }
        if payload is not None:
            # The API expects a payload of type bytes.
            converted_payload = payload.encode()

            # Add the payload to the request.
            task['app_engine_http_request']['body'] = converted_payload

        if in_seconds is not None:
            # Convert "seconds from now" into an rfc3339 datetime string.
            d = datetime.datetime.utcnow() + datetime.timedelta(seconds=in_seconds)

            # Create Timestamp protobuf.
            timestamp = timestamp_pb2.Timestamp()
            timestamp.FromDatetime(d)

            # Add the timestamp to the tasks.
            task['schedule_time'] = timestamp

            # Use the client to build and send the task.
            response = client.create_task(parent, task)

            print('Created task {}'.format(response.name))
        return render_template("success")
    else:
        return render_template("failure")


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





if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_flex_quickstart]
