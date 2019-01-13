from flask import Flask, request
import ML.models as models
from flask_mail import Mail,Message
import numpy as np


app = Flask(__name__)
mail = Mail(app)

# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
account_sid = 'AC777723e8b0ab0413f8952924f79c3bf2'
auth_token = '5687727831c1161956aefe046f9b56ff'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Your model has finished... melting... 😆😆",
                     from_='+14803729727',
                     to='+14803729727'
                 )

print(message.sid)


@app.route('/train_handler',methods=['POST'])
def train_handler():
    modelType = request.args.get('selection', '')    
    if modelType in ["nn","knn","svm","rf", "dt"]:
        msg = Message("Finished Learning", sender="admin@ezmlmodel.com",
                recipients=[request.args.get("email")])
        models.run_model(modelType, **request.args)
        mail.send(msg)
        
        
    else:
        return "404"