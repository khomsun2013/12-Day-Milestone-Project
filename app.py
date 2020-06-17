from flask import Flask, render_template,redirect
import requests
import matplotlib.pyplot as plt
import datetime
from bokeh.charts import Histogram
from bokeh.embed import components
import pandas as pd

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
  '''
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
  return render_template('plot.html', url='/template/stock.png')
  '''
  print(sdate)
  print(sopen)
  print('pass')
  return
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

iris_df = pd.read_csv("data/iris.data",names=["Sepal Length", "Sepal Width", "Petal Length", "Petal Width", "Species"])
feature_names = iris_df.columns[0:-1].values.tolist()

# Create the main plot
def create_figure(current_feature_name, bins):
  p = Histogram(iris_df, current_feature_name, title=current_feature_name, color='Species', bins=bins, legend='top_right', width=600, height=400)

  # Set the x axis label
  p.xaxis.axis_label = current_feature_name

  # Set the y axis label
  p.yaxis.axis_label = 'Count'
  return p

@app.route('/iris')
def iris():
  # Determine the selected feature
  current_feature_name = request.args.get("feature_name")
  if current_feature_name == None:
    current_feature_name = "Sepal Length"

  # Create the plot
  plot = create_figure(current_feature_name, 10)
    
  # Embed plot into HTML via Flask Render
  script, div = components(plot)
  return render_template("iris.html", script=script, div=div,feature_names=feature_names,  current_feature_name=current_feature_name)
  
if __name__ == '__main__':
  #app.run(port=33507)
  app.run()
