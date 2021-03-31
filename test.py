# import json
# data = {'{"UserID":"ID","UserGPS":"2.304055","worldStatus":"efewfwe"}': ''}
# datavalues = []
# for x in data :
#     datavalues.append(x)
# for data in datavalues:
#     #print(data[0])
#     row = json.loads(data)
#     print(row['UserID'])

import pandas as pd 
from datetime import datetime

import math


# def weeklyTweetSearch(beginWeek, endWeek):
#     # print(beginWeek,endWeek)
#     print('*'*20)
#     print("First",beginWeek, "Second", endWeek)
#     # Enter your keys/secrets as strings in the following fields
#     credentials = {}
#         credentials['CONSUMER_KEY'] = 'CONSUMER_KEY'
#         credentials['CONSUMER_SECRET'] = 'CONSUMER_SECRET'
#         credentials['ACCESS_TOKEN'] = 'ACCESS_TOKEN'
#         credentials['ACCESS_SECRET'] = 'ACCESS_SECRET'

#         # Save the credentials object to file
#         with open("twitter_credentials.json", "w") as file:
#             json.dump(credentials, file)

#         #Load credentials from json file
#         with open("twitter_credentials.json", "r") as file:
#             creds = json.load(file)

#         # Instantiate an object
#         python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

#         # Create our query
#         query = {'q': 'from:'+username,
#                 'result_type': 'mixed',
#                 #'geocode':'5.5720,7.0588,1446mi', #6.465422,3.406448,446mi
#                 'count': 3200
#                 # 'lang': 'en'
#                 }



#         # Search tweets
#         dict_ = {'user': [], 'date': [], 'text': [], 'favorite_count': []}
#         for status in python_tweets.search(**query)['statuses']:
#             dict_['user'].append(status['user']['screen_name'])
#             dict_['date'].append(status['created_at'])
#             dict_['text'].append(status['text'])
#             dict_['favorite_count'].append(status['favorite_count'])

#         # Structure data in a pandas DataFrame for easier manipulation
#         df = pd.DataFrame(dict_)
#         df.to_csv('exportTweets.csv', sep=',', encoding='utf-8',quotechar='"')
     

    
    

def get_Semantic_intent():

    dateToday = datetime.today().strftime('%Y-%m-%d')
    print("***",dateToday)
    
    print("&&&&")
    print(pd.date_range(start='1/1/2018',end=dateToday, freq='W',closed=None))
    print("&&&&")

    #remember mm/dd/year
    #dateRange = pd.date_range(start='1/1/2018',end=dateToday, freq='W',closed=None)
    #dateRange = pd.date_range(start='2/1/2018',end=dateToday, freq='W',closed=None)
    #dateRange = pd.date_range(start='7/1/2019',end=dateToday, freq='W',closed=None)
    dateRange = pd.date_range(start='7/1/2019',end=dateToday, freq='W',closed=None)

    print("days", len(str(dateRange)))
    print("days**", len(dateRange))

    numberOfWeeks = dateRange.shape[0]
    lastindex = numberOfWeeks - 1

    print("last Day",dateRange[lastindex])
    SplitdateRange = str(dateRange[1]).split(" ")
    print(SplitdateRange[0],"**")

    for date in dateRange:
        splitdate = str(date).split(" ")
        print (splitdate[0])

    # modulus = numberOfWeeks % 7
    # quotient = numberOfWeeks / 7


    # print('modulus',modulus)
    # print('quotient',quotient)

    

    # if modulus == 0:
    #     print('divisible by 7')
    #     number_of_iterations = quotient
    #     print('number of iterations',number_of_iterations)
    # else:
    #     print('non divisible by 7')
    #     quotient = math.floor(quotient)
    #     updatedQuotient = quotient + 1
    #     number_of_iterations = updatedQuotient
    #     print('number of iterations',number_of_iterations)



    numberOfWeeks = dateRange.shape[0]
    print(dateRange.length,"&&&&")
    lastindex = numberOfWeeks - 1
    # modulus = numberOfWeeks % 2
    # quotient = numberOfWeeks / 2

    if numberOfWeeks > 50:
        print("no support for more than 52 weeks in test API. Current number of weeks",numberOfWeeks)
    else :
        print("about to pull tweets***")
        for i in reversed(range(numberOfWeeks)):
            #if i != lastindex:
            if i != 0:
                j = i - 1
                print(j)
                WeekOne  = str(dateRange[i]).split(" ")
                WeekTwo  = str(dateRange[j]).split(" ")
                #weeklyTweetSearch(WeekOne[0],WeekTwo[0])
                #print("First",WeekOne, "Second", WeekTwo)

get_Semantic_intent()