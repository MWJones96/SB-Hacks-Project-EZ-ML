# SB-Hacks
SB Hacks project

## Technologies
Google Cloud Storage as a CDN
Google App Engine for hosting Python and Flask
Google Kubernetes? for training ML models
Twitter Bootstrap for UI
HTML5, CSS, and JS for the frontend
Python and Flask for the backend
Twilio API for 

## GCP Setup
Create a GCP Account
Enable the app engine interface
Download the command line interface.
Do the CLI setup
Git clone our repo
`cd` into repo
To sync the files in static `gsutil -m rsync -r ./static gs://sbhacks-static-bucket/static`  --- you guys can't do this step
Push to cloud with `gcloud deploy app`
