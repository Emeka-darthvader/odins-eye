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
#from flask import Flask,jsonify, request, render_template , flash ,url_for, send_from_directory

def scanUserData(username):
    
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

    username_parameter  = "from:"+username

    # Create our query
    query = {'q': username_parameter,
                'result_type': 'recent',
                #'geocode':'5.5720,7.0588,1446mi', #6.465422,3.406448,446mi
                'count': 100,
                'until':'2020-05-03'
                # 'lang': 'en'
                }

    # query = {'user_id':username}


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
    return "ok"
    
scanUserData("i_am_emeka") #get tweets for my account @i_am_emeka
