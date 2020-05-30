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

dateToday = datetime.today().strftime('%Y-%m-%d')
print("***",dateToday)
print(pd.date_range(start='1/1/2018',end=dateToday, freq='W',closed=None))

dateRange = pd.date_range(start='1/1/2018',end=dateToday, freq='W',closed=None)
print(dateRange[1])