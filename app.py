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
    ## edited from https://pynative.com/python-generate-random-string/
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


#******************beginning Safe Space APIs



@app.route('/generateAPIKEY',methods=['GET','POST'])
def generateAPIKey():
    if (request.method == 'GET'):
        APIKey = generateRandomAPIKey()
        Length = len(APIKey)
        return jsonify({'API Key' : APIKey,'Length':Length}),201
    else:
        resultant = 'Kindly check documentation for the right parameters.'
        return jsonify({'Response': resultant})



@app.route('/safe-space/post-world-view',methods=['GET','POST'])
def postWorldView():
    if request.method == 'POST':
        if request.is_json:
            
            API_Key = request.args.get('APIKey')

            #if API_Key == "z16(iTUrN>g.n,%/$-mE<JQ[" :
            if API_Key == "zdakenkwrWQER12vevlfwrfwke23134" :
                data = request.get_json()
                UserID = data['UserID']
                UserGPS = data['UserGPS']
                WorldView = data['WorldView']
                
                new_user = UsersModel(UserID=data['UserID'])
                new_history = UsersHistoryModel(UserID=data['UserID'], UserGPS=data['UserGPS'], WorldView=data['WorldView'])
                
                existing_user = db.session.query(db.exists().where(UsersModel.UserID==data['UserID'])).scalar()
                if existing_user == True:
                    db.session.add(new_history)
                    db.session.commit()
                    return jsonify({"message": "User already exists. Committed History"})
                
                db.session.add(new_user)
                db.session.add(new_history)
                db.session.commit()
                return jsonify({"message": f"User {new_user.UserID}  and {new_history.UserID} has been created successfully."})
            else:
                return jsonify({"message": f"Invalid APIKey"})
        else:
            API_Key = request.args.get('APIKey')

            #if API_Key == "z16(iTUrN>g.n,%/$-mE<JQ[" :
            if API_Key == "zdakenkwrWQER12vevlfwrfwke23134" :

                data = request.form.to_dict()
                datavalues = []
                for x in data :
                    datavalues.append(x)
                for data in datavalues:
                    #print(data["userID"])
                    row = json.loads(data)
                #data = json.loads(request.data)
                    UserID = row['UserID']
                    UserGPS = row['UserGPS']
                    WorldView = row['worldStatus']
                
                    new_user = UsersModel(UserID=row['UserID'])
                    new_history = UsersHistoryModel(UserID=row['UserID'], UserGPS=row['UserGPS'], WorldView=row['worldStatus'])
                
                    existing_user = db.session.query(db.exists().where(UsersModel.UserID==row['UserID'])).scalar()
                    if existing_user == True:
                        db.session.add(new_history)
                        db.session.commit()
                        # return jsonify({"message": "User already exists. Committed History"})
                        #message  = "User already exists. Committed History",
                        #return message
                        return jsonify({"message": "User already exists. Committed History"})
                
                    db.session.add(new_user)
                    db.session.add(new_history)
                    db.session.commit()
                    #message = "User {new_user.UserID}  and {new_history.UserID} has been created successfully."
                    return jsonify({"message": f"User {new_user.UserID}  and {new_history.UserID} has been created successfully."})
                return jsonify({"message": f"User {new_user.UserID}  and {new_history.UserID} has been created successfully."})
                #return message

            else:
                return jsonify({"message": f"Invalid APIKey"})
        # else:
        #     return jsonify({"error": "The request payload is not in JSON format1"})
        



@app.route('/users',methods=['GET','POST'])
def getUsers():
    if request.method == 'POST':
        return jsonify({"error": "No POST action allowed"})
        # if request.is_json:
        #     data = request.get_json()
        #     new_user = UsersModel(firstName=data['firstName'], lastName=data['lastName'], email=data['email'],password=data['password'],secret=data['secret'])
        #     db.session.add(new_user)
        #     db.session.commit()
        #     return jsonify({"message": f"User {new_user.UserID} has been created successfully."})
        # else:
            # return jsonify({"error": "The request payload is not in JSON format"})

    elif request.method == 'GET':
        users = UsersModel.query.all()
        results = [
            {
                "User_ID": user.UserID,
                # "Last name": user.lastName,
                # "Email": user.email
            } for user in users]

        return jsonify({"count": len(results), "users": results})

@app.route('/history',methods=['GET','POST'])
def getHistory():
    if request.method == 'POST':
        return jsonify({"error": "No POST action allowed"})
        # if request.is_json:
        #     data = request.get_json()
        #     new_user = UsersModel(firstName=data['firstName'], lastName=data['lastName'], email=data['email'],password=data['password'],secret=data['secret'])
        #     db.session.add(new_user)
        #     db.session.commit()
        #     return jsonify({"message": f"User {new_user.UserID} has been created successfully."})
        # else:
            # return jsonify({"error": "The request payload is not in JSON format"})

    elif request.method == 'GET':
        users = UsersHistoryModel.query.all()
        results = [
            {
                "User_ID": user.UserID,
                "User_GPS": user.UserGPS,
                "WorldView": user.WorldView
            } for user in users]

        return jsonify({"count": len(results), "Historical Data Count": results})


#******************End of Safe Space APIs

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
        credentials['CONSUMER_KEY'] = 'guDZwytCrIRP3m8OAZKEHJ37e'
        credentials['CONSUMER_SECRET'] = 'HNlEpqrUnIkcMByabUH52stSUl1CqcjA7KEe0v5MNjaSMLqJM7'
        credentials['ACCESS_TOKEN'] = '917684338065539072-RhO82gMbWRDtYDJcndGVOwG4Y5jevlt'
        credentials['ACCESS_SECRET'] = 'QUJGS8CU35zmOHJYNQ2RVTKEsF5Brmj3laqvRqqm1MKbc'

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
