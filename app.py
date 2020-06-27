from flask import Flask,render_template,redirect,flash,url_for,request
import requests
import datetime
import pandas as pd
from bokeh.io import output_file, show, save
from bokeh.layouts import column
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, CustomJS
from bokeh.models.widgets import Button
import os

import sqlite3

app = Flask(__name__)

DATABASE = 'Companylist.db'

conn = sqlite3.connect('Companylist.db')

c=conn.cursor()

@app.route('/')
def index():
  return render_template('index.html')

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response  

@app.route('/nasdaq')
def nasdaq():
  c.execute('SELECT symbol,name FROM NASDAQ')
  tup=c.fetchall()
  return render_template('nasdaq.html',data=tup)

@app.route('/amex')
def amex():
  c.execute('SELECT symbol,name FROM AMEX')
  tup=c.fetchall()
  return render_template('amex.html',data=tup)

@app.route('/nyse')
def nyse():
  c.execute('SELECT symbol,name FROM NYSE')
  tup=c.fetchall()
  return render_template('nyse.html',data=tup)

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/stock',methods=['GET','POST'])
def stock():
  try:
    if (request.method == 'POST'):
      default_name = 'AAPL'
      default_value = 0
      #stocks = request.args.get("stocks",default_name) 
      #iopen = int(request.args.get('Open', default_value))
      #ihigh = int(request.args.get('High', default_value))
      #ilow = int(request.args.get('Low', default_value))
      #iclose = int(request.args.get('Close', default_value))
      stocks = request.values.get("stocks",default_name) 
      iopen = int(request.values.get('Open', default_value))
      ihigh = int(request.values.get('High', default_value))
      ilow = int(request.values.get('Low', default_value))
      iclose = int(request.values.get('Close', default_value))
      #return render_template("about.html", content=stocks,content1=[iopen,ihigh,ilow,iclose])
      if (iopen+ihigh+ilow+iclose)==0:
        return render_template('index.html')

      #if os.path.exists("./templates/stocks.html"):
      #  os.remove("./templates/stocks.html")
      #else:
      #  print("The file does not exist")
      
      '''
      sel=[0,0,0,0]
      dst = request.form.to_dict()
      if('Open' in dst): sel[0]=1
      if('High' in dst): sel[1]=2 
      if('Low' in dst): sel[2]=3
      if('Close' in dst): sel[3]=4
      if sum(sel)==0:
        return render_template('index.html')
      '''
      r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+stocks+'&outputsize=compact&apikey=HGGFPH8DG45PWMAB')
      data = r.json()
      dic = data['Time Series (Daily)']
      pdic=pd.DataFrame(dic)
      pdic=pdic.T
      x=range(1,31)
      pd30 = pdic.head(30)
      #output_file('./templates/stocks.html')
      output_file('./templates/'+stocks+str(iopen)+str(ihigh)+str(ilow)+str(iclose)+'.html',mode='inline')
      p2 = figure(title='Stock Prices '+stocks+' Back in 30 Days', x_axis_label='Date',y_axis_label='Price')
      grpo=['Open']*30
      grph=['High']*30
      grpl=['Low']*30
      grpc=['Close']*30
      grp_list=['Open','High','Low','Close']
      colors=['green','orange','blue','red']
      if(iopen==1):
        source = ColumnDataSource(
        data={'x':x,
              'date':list(pd30.index.values),
              'group':grpo,
              'y':list(pd30['1. open'].values)})
        p2.line(x='x',y='y',source=source,legend_label = grp_list[0],color = colors[0])
        p2.circle(x='x', y='y', fill_color=colors[0],line_color=colors[0], size=8,source=source,legend_label = grp_list[0])
      if(ihigh==2):
        source = ColumnDataSource(
        data={'x':x,
              'date':list(pd30.index.values),
              'group':grph,
              'y':list(pd30['2. high'].values)})
        p2.line(x='x',y='y',source=source,legend_label = grp_list[1],color = colors[1])
        p2.circle(x='x', y='y', fill_color=colors[1],line_color=colors[1], size=8,source=source,legend_label = grp_list[1])
      if(ilow==3):
        source = ColumnDataSource(
        data={'x':x,
              'date':list(pd30.index.values),
              'group':grpl,
              'y':list(pd30['3. low'].values)})
        p2.line(x='x',y='y',source=source,legend_label = grp_list[2],color = colors[2])
        p2.circle(x='x', y='y', fill_color=colors[2],line_color=colors[2], size=8,source=source,legend_label = grp_list[2])
      if(iclose==4):
        source = ColumnDataSource(
        data={'x':x,
              'date':list(pd30.index.values),
              'group':grpc,
              'y':list(pd30['4. close'].values)})
        p2.line(x='x',y='y',source=source,legend_label = grp_list[3],color = colors[3])
        p2.circle(x='x', y='y', fill_color=colors[3],line_color=colors[3], size=8,source=source,legend_label = grp_list[3])
      '''
      for i in range(len(sel)):
        if(sel[i]==1):
          source = ColumnDataSource(
          data={'x':x,
                'date':list(pd30.index.values),
                'group':grpo,
                'y':list(pd30['1. open'].values)})
          p2.line(x='x',y='y',source=source,legend_label = grp_list[i],color = colors[i])
          p2.circle(x='x', y='y', fill_color=colors[i],line_color=colors[i], size=8,source=source,legend_label = grp_list[i])
        if(sel[i]==2):
          source2= ColumnDataSource(
          data={'x':x,
                'date':list(pd30.index.values),
                'group':grph,
                'y':list(pd30['2. high'].values)})
          p2.line(x='x',y='y',source=source2,legend_label = grp_list[i],color = colors[i])
          p2.circle(x='x', y='y', fill_color=colors[i],line_color=colors[i], size=8,source=source2,legend_label = grp_list[i])
        if(sel[i]==3):
          source3 = ColumnDataSource(
          data={'x':x,
                'date':list(pd30.index.values),
                'group':grpl,
                'y':list(pd30['3. low'].values)})
          p2.line(x='x',y='y',source=source3,legend_label = grp_list[i],color = colors[i])
          p2.circle(x='x', y='y', fill_color=colors[i],line_color=colors[i], size=8,source=source3,legend_label = grp_list[i])
        if(sel[i]==4):
          source4 = ColumnDataSource(
          data={'x':x,
                'date':list(pd30.index.values),
                'group':grpc,
                'y':list(pd30['4. close'].values)})
          p2.line(x='x',y='y',source=source4,legend_label = grp_list[i],color = colors[i])
          p2.circle(x='x', y='y', fill_color=colors[i],line_color=colors[i], size=8,source=source4,legend_label = grp_list[i])
      '''
      hover = HoverTool(tooltips =[('Type: ','@group'),('Date: ','@date'),('Price: ','@y')])
      p2.add_tools(hover)
      #show(p2)
      #return 
      save(p2)
      return render_template(stocks+str(iopen)+str(ihigh)+str(ilow)+str(iclose)+'.html')
  except Exception as e:
      print(e)
      #flash(e)
      return render_template('index.html')
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

if __name__ == '__main__':
  #app.run(port=33507)
  app.run(debug='True')
'''
'''      
