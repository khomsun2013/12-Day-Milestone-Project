from flask import Flask, render_template, request, redirect
import simplejson as json
import requests

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/stock')
def stock():
  # api-endpoint 
  URL = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&outputsize=full&apikey=demo"
  # location given here 
  #location = "delhi technological university"
  # defining a params dict for the parameters to be sent to the API 
  #PARAMS = {'address':location} 
  # sending get request and saving the response as response object 
  r = requests.get(url = URL)#, params = PARAMS) 
  # extracting data in json format 
  data = r.json()
  print(data['Time Series (Daily)'][0])
  return None  

if __name__ == '__main__':
  app.run(port=33507)
