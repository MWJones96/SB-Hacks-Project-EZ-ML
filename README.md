# EZ ML

SB Hacks project: a web app for building your own machine learning model by uploading CSV data, choosing a scikit-learn classifier and setting its parameters.

## Overview

EZ ML was built over a weekend at SB Hacks in January 2019. The idea was that a user uploads training data, training targets and test data as CSV files, picks a classifier, adjusts its hyperparameters in a form, and leaves an email address and phone number. Training would run in the background on Google Cloud, and the user would be emailed a CSV of predictions and sent a text message when the model had finished.

The repository is a hackathon prototype. The front end and the classifier wrappers are in place, but the back end was not finished and does not run as committed (see [Status and limitations](#status-and-limitations)).

## What's implemented

- **Landing page and form** (`templates/index.html`): Bootstrap 4 page with Home, About, Team and Try sections, file inputs for training data, training targets and test data, a classifier selector, email and phone fields, and a **Configure parameters** button that inserts the parameter form for the chosen classifier.
- **Parameter forms** for five classifiers, with fields matching the scikit-learn arguments used:

  | Classifier | Template | Parameters |
  |------------|----------|------------|
  | Neural network (`MLPClassifier`) | `mlp.html` | `hidden_layer_sizes`, `alpha`, `learning_rate_init`, `power_t`, `max_iter`, `tol`, `momentum`, `validation_fraction`, `beta_1`, `beta_2`, `epsilon`, `n_iter_no_change`, `shuffle` |
  | K-nearest neighbours (`KNeighborsClassifier`) | `knn.html` | number of neighbours, leaf size, `p` |
  | Support vector machine (`SVC`) | `svm.html` | `C`, `kernel`, `degree`, `coef0`, `shrinking`, `probability`, `tol`, `cache_size`, `max_iter` |
  | Random forest (`RandomForestClassifier`) | `rf.html` | `min_samples_split`, `min_samples_leaf`, `min_weight_fraction_leaf`, `min_impurity_decrease` |
  | Decision tree (`DecisionTreeClassifier`) | `dt.html` | `min_samples_split`, `min_samples_leaf`, `min_weight_fraction_leaf`, `min_impurity_decrease` |

- **Model wrappers** (`ML/`): one function per classifier that fits on the training data and returns predictions for the test data, plus `models.run_model`, which dispatches on a model code (`nn`, `knn`, `svm`, `rf`, `dt`).
- **Flask back end** (two drafts):
  - `main.py` saves the three uploaded files to Google Cloud Storage under a SHA-256 hash of the user's email and queues a training job with Google Cloud Tasks.
  - `main2.py`, the entry point named in `app.yaml`, saves the files the same way and runs training in a separate process, then sends an email with Flask-Mail and a text message with Twilio.
- **Task handler** (`teskHandler/handler.py`): a `/train_handler` endpoint intended to receive queued training jobs, and `mymail.py`, an SMTP email helper.
- **Sample data** (`Sample Data/`): `raw_data.csv` (569 rows; its columns match the Breast Cancer Wisconsin (Diagnostic) dataset), with `extract_data.py` to split it into feature data (`data.csv`) and diagnosis targets (`targets.csv`).

## Tech stack

- **Front end**: HTML5 Boilerplate, Bootstrap 4.1, jQuery 3.3, Popper.js, Jinja2 templates
- **Back end**: Python 3, Flask, Flask-Mail, gunicorn
- **Machine learning**: scikit-learn, NumPy, SciPy
- **Cloud**: Google App Engine (flexible environment), Google Cloud Storage, Google Cloud Tasks (`main.py` only)
- **Notifications**: Twilio (SMS), email via Flask-Mail or SMTP

Pinned Python dependencies are listed in `requirements.txt`.

## Getting started

### Prerequisites

- Python 3 (`app.yaml` sets `python_version: 3`; the dependency pins date from early 2019, for example Flask 1.0.2 and scikit-learn 0.20.2).
- For deployment: a Google Cloud project with App Engine enabled, the Google Cloud SDK (`gcloud` and `gsutil`), and a Cloud Storage bucket.
- For notifications: your own Twilio account and email credentials.

### Configuration

`main2.py` and `teskHandler/mymail.py` import credentials (`SID`, `TOKEN`, `FROMADDR`, `FROMPASS`) from a `constants.py` module, which is excluded by `.gitignore` and must be created locally with your own values. The Cloud Storage bucket names are set in `app.yaml` and at the top of `main.py` and `main2.py`.

### Install

```sh
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Run locally

Both Flask drafts end with a development server on `127.0.0.1:8080`:

```sh
python main2.py
```

As committed, this fails at import time; see below.

### Deploy to Google App Engine

From the original setup notes:

1. Create a Google Cloud account and enable App Engine.
2. Install and initialise the Google Cloud SDK.
3. Clone the repository and `cd` into it.
4. Sync the static assets to your Cloud Storage bucket, for example `gsutil -m rsync -r ./static gs://<your-bucket>/static`.
5. Deploy with `gcloud app deploy`.

`app.yaml` runs `gunicorn -b :$PORT main2:app` on a single manual-scaled instance (1 CPU, 0.5 GB memory).

## Project structure

```
main.py               Flask draft: uploads to Cloud Storage, queues jobs with Cloud Tasks
main2.py              Flask draft used by app.yaml: uploads, background training, email and SMS
main_test.py          App Engine sample test for the index route
app.yaml              App Engine flexible environment configuration
requirements.txt      Pinned Python dependencies
processModel.js       Submit listener that logs the email and classifier (not loaded by any template)
ML/                   scikit-learn classifier wrappers and the run_model dispatcher
teskHandler/          Training task handler and SMTP email helper
templates/            Jinja2 templates: landing page, parameter forms, success, failure, 404
static/               HTML5 Boilerplate assets, CSS, JavaScript, images and icons
Sample Data/          Sample dataset and CSV preparation scripts
```

## Tests

`main_test.py` is the test from Google's App Engine "hello world" sample. It requests `/` and asserts that the response contains "Hello World", which the EZ ML landing page does not, so it will fail even once the import errors are fixed. It can be run with pytest:

```sh
pip install pytest
pytest main_test.py
```

## Status and limitations

This is unfinished hackathon code. Known problems include:

- `main.py` and `main2.py` import names that do not exist (`allowed_file` and `secure_filename` from `flask`, `google.storage`, and a `LOCATION_ID` module), so neither starts.
- The form posts to `search`, but the upload route is `/req`; the form also lacks `enctype="multipart/form-data"`, which file uploads require.
- The front end uses the model code `neural-net`, while `models.run_model` and `trainer` expect `nn`.
- `run_model("dt", ...)` calls `dt.neural_network` instead of `dt.decision_tree`.
- `save_files` reads a `test-targets` file that the form does not send, and writes it over the `train-data` object.
- `main.py` references undefined variables (`in_seconds`, `datetime`) when creating Cloud Tasks.
- `Sample Data/data.csv` contains unresolved Git merge-conflict markers; regenerate it with `extract_data.py`. `datatoarray.py` uses Python 2 `print` syntax.
- The "Google Kubernetes" training back end mentioned in the original notes was never implemented.
- The `ML/__pycache__/` directory with compiled `.pyc` files is committed.
- `teskHandler/handler.py` contains hard-coded Twilio credentials and sends a test SMS as soon as it is imported. Do not use those credentials; move them to `constants.py` with your own values.

## Licence

Released under the GNU General Public License v3.0. See [LICENSE](LICENSE).

## Acknowledgements

- Built at SB Hacks. The original repository was `TheEighthByte/SB-Hacks`.
- Contributors, as recorded in the commit history: Matthew Jones, Eric Y, Austin Zuo and darhsu.
- Built with scikit-learn, Flask, Bootstrap, HTML5 Boilerplate, Google Cloud and Twilio.
