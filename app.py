from flask import Flask, render_template,redirect
#from alpha_vantage.timeseries import TimeSeries
#from pprint import pprint

#import simplejson as json
import requests
#import urllib.request as urllib2
import json
import matplotlib.pyplot as plt
import datetime
import numpy as np

'''
req = urllib2.Request("http://api.open-notify.org/iss-now.json")
response = urllib2.urlopen(req)

obj = json.loads(response.read())

print (obj['timestamp'])
print (obj['iss_position']['latitude'], obj['iss_position']['longitude'])
'''

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/stock')
def stock():
  '''
  req = urllib2.Request("http://api.open-notify.org/iss-now.json")
  response = urllib2.urlopen(req)
  obj = json.loads(response.read())
  print (obj['timestamp'])
  print (obj['iss_position']['latitude'], obj['iss_position']['longitude'])
  '''
  '''
  r = requests.get("http://api.open-notify.org/iss-now.json")
  print(r.status_code)
  data = r.json()
  print(data['timestamp'])
  print(data['iss_position']['latitude'], data['iss_position']['longitude'])
  return render_template('plot.html', url='plot.png')
  '''
  
  r = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&outputsize=full&apikey=HGGFPH8DG45PWMAB")
  data = r.json()
  dic = data['Time Series (Daily)']
  tod = datetime.datetime.now()
  sdate=[]
  sopen=[]
  shigh=[]
  slow=[]
  sclose=[]
  svol=[] 
  for i in range(1,8):
    d = datetime.timedelta(days = i)
    a = tod - d
    dt = str(a.date())
    if dt in dic:
      sdate.append(dt)
      sopen.append(float(dic[dt]['1. open']))
      shigh.append(float(dic[dt]['2. high']))
      slow.append(float(dic[dt]['3. low']))
      sclose.append(float(dic[dt]['4. close']))
      svol.append(float(dic[dt]['5. volume']))
  
  plt.figure()#figsize=(9, 3))
  plt.subplot(221)
  plt.plot(sdate,sclose)
  plt.subplot(222)
  plt.plot(sdate,sclose)
  plt.subplot(223)
  plt.plot(sdate,sclose)
  plt.subplot(224)
  plt.plot(sdate,sclose)
  plt.suptitle('Categorical Plotting')
  plt.savefig('/template/stock.png')
  print('pass')
  return render_template('plot.html', url='/template/stock.png')
  #plt.show()  

  '''
  ts = TimeSeries(key='HGGFPH8DG45PWMAB',retries='20',output_format='pandas')
  data, meta_data = ts.get_intraday(symbol='IBM',interval='1min', outputsize='full')
  pprint(data.head(2))
  '''
  # api-endpoint
  #URL = "http://api.open-notify.org/iss-now.json"
  #URL = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&outputsize=full&apikey=HGGFPH8DG45PWMAB"
  #URL = "https://docs.google.com/spreadsheets/d/1dKmaV_JiWcG8XBoRgP8b4e9Eopkpgt7FL7nyspvzAsE"
  # location given here 
  #location = "delhi technological university"
  # defining a params dict for the parameters to be sent to the API 
  #PARAMS = {'address':location} 
  # sending get request and saving the response as response object 
  #r = requests.get("http://api.open-notify.org/iss-now.json")
  #print(r.status_code)
  # extracting data in json format 
  #data = r.json()
  #print(data['Time Series (Daily)'][0])
  
if __name__ == '__main__':
  #app.run(port=33507)
  app.run()
