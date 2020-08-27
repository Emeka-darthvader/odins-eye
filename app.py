from flask import Flask,jsonify, request, render_template , flash ,url_for, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug import secure_filename
import json
import requests
import random
import string
import os
import hashlib,binascii
# from flask_login import LoginManager,current_user, login_user,UserMixin, logout_user

#for odin's eye
from twython import Twython
# import json
import csv
import json
import pandas as pd
import re
import nltk 
from nltk.tokenize import word_tokenize
from string import punctuation 
from nltk.corpus import stopwords 
import pickle



#from models import Result


app = Flask(__name__)
# login = LoginManager(app)

CORS(app)

#put DB details
#app.config['SQLALCHEMY_DATABASE_URI'] = "host:port/dbName"


db = SQLAlchemy(app)
migrate = Migrate(app, db)

UPLOAD_DIRECTORY = "static/models/"

class UsersModel(db.Model):
    #class UsersModel(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.String())
    

    def __init__(self, UserID):
        self.UserID = UserID
        
        
    def __repr__(self):
        return f"< {self.UserID}>"

class UsersHistoryModel(db.Model):
    #class UsersModel(UserMixin,db.Model):
    __tablename__ = 'users_history'

    id = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.String())
    UserGPS = db.Column(db.String())
    WorldView = db.Column(db.String())
    

    def __init__(self, UserID, UserGPS, WorldView):
        self.UserID = UserID
        self.UserGPS = UserGPS
        self.WorldView = WorldView
        
    def __repr__(self):
        return f"< {self.UserID}>"

def generateRandomAPIKey():
    otherText = string.ascii_letters + string.digits + string.punctuation
    password = random.choice(string.ascii_lowercase)
    password += random.choice(string.ascii_uppercase)
    password += random.choice(string.digits)
    password += random.choice(string.punctuation)

    for i in range(20):
        password += random.choice(otherText)

    passwordList = list(password)
    random.SystemRandom().shuffle(passwordList)
    password = ''.join(passwordList)
    return password

"hashing code"
def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')
 
def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

# @login.user_loader
# def load_user(id):
#     return UsersModel.query.get(int(id))

@app.route('/',methods=['GET','POST'])
def index():
    if (request.method == 'POST'):
        some_json = request.get_json()
        return jsonify({'you sent' : some_json}),201
    else:
        resultant = 'Welcome!!'
        return jsonify({'Scuudu Web APIs': resultant})



#******************beginning of odins-eye
@app.route('/odins-eye/',methods=['GET','POST'])
def welcomeOdinsEye():
    if (request.method == 'GET'):
        return jsonify({'Welcome' : 'Welcome to Odin\'s Eye API'}),201
    else:
        resultant = 'Kindly check documentation for the right parameters.'
        return jsonify({'Response': resultant})


@app.route('/odins-eye/scan-user/<string:username>',methods=['GET','POST'])
def scanUserData(username):
    if (request.method == 'GET'):
        # Enter your keys/secrets as strings in the following fields
        credentials = {}
        credentials['CONSUMER_KEY'] = 'CONSUMER_KEY'
        credentials['CONSUMER_SECRET'] = 'CONSUMER_SECRET'
        credentials['ACCESS_TOKEN'] = 'ACCESS_TOKEN'
        credentials['ACCESS_SECRET'] = 'ACCESS_SECRET'

        # Save the credentials object to file
        with open("twitter_credentials.json", "w") as file:
            json.dump(credentials, file)

        #Load credentials from json file
        with open("twitter_credentials.json", "r") as file:
            creds = json.load(file)

        # Instantiate an object
        python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

        # Create our query
        query = {'q': 'from:'+username,
                'result_type': 'mixed',
                #'geocode':'5.5720,7.0588,1446mi', #6.465422,3.406448,446mi
                'count': 3200
                # 'lang': 'en'
                }



        # Search tweets
        dict_ = {'user': [], 'date': [], 'text': [], 'favorite_count': []}
        for status in python_tweets.search(**query)['statuses']:
            dict_['user'].append(status['user']['screen_name'])
            dict_['date'].append(status['created_at'])
            dict_['text'].append(status['text'])
            dict_['favorite_count'].append(status['favorite_count'])

        # Structure data in a pandas DataFrame for easier manipulation
        df = pd.DataFrame(dict_)
        df.to_csv('exportTweets.csv', sep=',', encoding='utf-8',quotechar='"')
        return jsonify({'Welcome' : 'Welcome to Odin\'s Eye API'}),201
    else:
        resultant = 'Kindly check documentation for the right parameters.'
        return jsonify({'Response': resultant})




#******************end of odins-eye



# @app.route("/downloadFile/<path:path>")
# def get_file(path):
#     """Download a file."""
#     return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


# if __name__ == '__main__':
#     app.run(debug=True)
