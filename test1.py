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

import tweepy
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


with open("twitter_credentials.json", "r") as file:
    username = "i_am_emeka"
    creds = json.load(file)

    ##Twython
    # Instantiate an object
    python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

    

    # Create our query
    query = {'q': 'from:'+username,
    'result_type': 'mixed',
    #'geocode':'5.5720,7.0588,1446mi', #6.465422,3.406448,446mi
    'count': 3200,
    
    # 'lang': 'en'
    }



    # Search tweets
    dict_ = {'user': [], 'date': [], 'text': [], 'favorite_count': []}
    for status in python_tweets.search(**query,tweet_mode="extended")['statuses']:

        #print("dict",status)
        
        if 'retweeted_status' in status:
            # print('true')
            # print(status['retweeted_status']['full_text'])
            # print('#'*20)
            dict_['user'].append(status['user']['screen_name'].strip().replace("\r\n",""))
            dict_['date'].append(status['created_at'].strip().replace("\n",""))
            dict_['text'].append(status['retweeted_status']['full_text'].strip().replace("\n",""))
            dict_['favorite_count'].append(status['favorite_count'])

        elif 'quoted_status' in status:
            print('*'*20)
            dict_['user'].append(status['user']['screen_name'].strip().replace("\r\n",""))
            dict_['date'].append(status['created_at'].strip().replace("\n",""))
            dict_['text'].append(status['quoted_status']['full_text'].strip().replace("\n",""))
            dict_['favorite_count'].append(status['favorite_count'])
            print('*'*20)
        else:
            print('*'*20)
            dict_['user'].append(status['user']['screen_name'].strip().replace("\r\n",""))
            dict_['date'].append(status['created_at'].strip().replace("\n",""))
            dict_['text'].append(status['full_text'].strip().replace("\n",""))
            dict_['favorite_count'].append(status['favorite_count'])
            print("*"*20)

        # dict_['user'].append(status['user']['screen_name'].strip().replace("\r\n",""))
        # dict_['date'].append(status['created_at'].strip().replace("\n",""))
        # dict_['text'].append(status['full_text'].strip().replace("\n",""))
        # dict_['favorite_count'].append(status['favorite_count'])

    # Structure data in a pandas DataFrame for easier manipulation
    df = pd.DataFrame(dict_)
    df.to_csv('newExport1.csv', sep=',', encoding='utf-8',quotechar='"',mode='w')


    # ####Tweepy
    # auth = tweepy.OAuthHandler(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
    # auth.set_access_token(creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])

    # api = tweepy.API(auth, wait_on_rate_limit=True)
    # search_words = "#wildfires"
    # date_since = "2018-11-16"

    # new_search = 'from:'+username

    # tweets = tweepy.Cursor(api.search,
    #     q=new_search,
    #     lang="en",
    #     since='2020-01-01',tweet_mode="extended").items(10000)

    # for tweet in tweets:
        
    #     print(tweet.full_text)
    #     print("*"*20)
     