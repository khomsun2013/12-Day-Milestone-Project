from flask import Flask, render_template,redirect
import requests
import matplotlib.pyplot as plt
import datetime
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource

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
  

  output_file("templates/stock.html")
  source = ColumnDataSource(data=dict(
    x=[i+1 for i in range(len(sdate)+1)],
    y1=sopen,
    y2=shigh,
    y3=slow,
    y4=sclose,
    y5=svol
  ))
  p = figure(plot_width=400, plot_height=400)
  p.vline_stack(['y1', 'y2', 'y3', 'y4', 'y5'], x='x', source=source)
  show(p)    
  return render_template('stock.html')

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

@app.route('/iris')
def iris():
  output_file("templates/bars.html")
  fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
  counts = [5, 3, 4, 2, 4, 6]
  p = figure(x_range=fruits, plot_height=250, title="Fruit Counts",toolbar_location=None, tools="")
  p.vbar(x=fruits, top=counts, width=0.9)
  p.xgrid.grid_line_color = None
  p.y_range.start = 0
  show(p)
  return render_template('bars.html')
  
if __name__ == '__main__':
  #app.run(port=33507)
  app.run()
