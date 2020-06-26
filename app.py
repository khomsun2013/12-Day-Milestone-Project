from flask import Flask,render_template,redirect,flash,url_for,request
import requests
import datetime
import pandas as pd
from bokeh.io import output_file, show, save
from bokeh.layouts import column
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, CustomJS
from bokeh.models.widgets import Button

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
      sel=[0]*4
      dst = request.form.to_dict()
      return render_template("about.html", content=dst)
      if('Open' in dst): sel[0]=1
      if('High' in dst): sel[1]=1 
      if('Low' in dst): sel[2]=1
      if('Close' in dst): sel[3]=1
      if sum(sel)==0:
        return render_template('index.html')
      r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+dst['stocks']+'&outputsize=full&apikey=HGGFPH8DG45PWMAB')
      data = r.json()
      dic = data['Time Series (Daily)']
      pdic=pd.DataFrame(dic)
      pdic=pdic.T
      x=range(1,31)
      pd30 = pdic.head(30)
      output_file('templates/stocks.html',mode='inline')
      #output_file('templates/'+dst['stocks']+'.html',mode='inline')
      p2 = figure(title='Stock Prices '+dst['stocks']+' Back in 30 Days', x_axis_label='Date',y_axis_label='Price')
      grpo=['Open']*30
      grph=['High']*30
      grpl=['Low']*30
      grpc=['Close']*30
      grp_list=['Open','High','Low','Close']
      colors=['green','orange','blue','red']
      for i in range(4):
        if(i==0)and(sel[0]==1):
          source = ColumnDataSource(
          data={'x':x,
                'date':list(pd30.index.values),
                'group':grpo,
                'y':list(pd30['1. open'].values)})
        elif(i==1)and(sel[1]==1):
          source = ColumnDataSource(
          data={'x':x,
                'date':list(pd30.index.values),
                'group':grph,
                'y':list(pd30['2. high'].values)})
        elif(i==2)and(sel[2]==1):
          source = ColumnDataSource(
          data={'x':x,
                'date':list(pd30.index.values),
                'group':grpl,
                'y':list(pd30['3. low'].values)})
        elif(i==3)and(sel[3]==1):
          source = ColumnDataSource(
          data={'x':x,
                'date':list(pd30.index.values),
                'group':grpc,
                'y':list(pd30['4. close'].values)})
        if sel[i]==1:  
          p2.line(x='x',y='y',source=source,legend_label = grp_list[i],color = colors[i])
          p2.circle(x='x', y='y', fill_color=colors[i],line_color=colors[i], size=8,source=source,legend_label = grp_list[i])
      hover = HoverTool(tooltips =[('Type: ','@group'),('Date: ','@date'),('Price: ','@y')])
      p2.add_tools(hover)
      save(p2)

      '''
      btn = Button(label="Back", button_type="success")
      btn.on_click(change_click)
      curdoc().add_root(bt)
      layout = column(p2,btn)
      save(layout)
      '''
      
      '''
      tod = datetime.datetime.now()
      sdate=[]
      sopen=[]
      shigh=[]
      slow=[]
      sclose=[]
      svol=[] 
      for i in range(1,30):
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
      x=[i+1 for i in range(len(sdate))]
      source_open = ColumnDataSource(data=dict(
          date=x,
          open=sopen,
          close=sclose,
          sdate=sdate,
      ))
      output_file('templates/'+dst['stocks']+'.html',mode='inline')
      #plot = figure(title='Stock IBM Daily', x_axis_label='Date',
      #                y_axis_label='Price',x_range=sdate)
      #plot.circle(sdate, sopen, fill_color="green",line_color='green', size=8)
      plot = figure(title='Stock '+dst['stocks']+' Back in 30 Days', x_axis_label='Date',y_axis_label='Price')
      plot.line('date', 'open', line_width=2, line_color='green', legend_label='Open', source=source_open)
      plot.circle('date', 'open', fill_color="green",line_color='green', size=8,source=source_open)
      plot.line('date', 'close', line_width=2, line_color='red', legend_label='Close', source=source_open)
      plot.circle('date', 'close', fill_color="red",line_color='red', size=8,source=source_open)
      #plot.line('date', sopen, line_width=3, line_color='green', legend_label='Open')
      #plot.line(x, shigh, line_width=3, line_color='orange', legend_label='High')
      #plot.line(x, slow, line_width=3, line_color='red', legend_label='Low')
      #plot.line(x, sclose, line_width=3, line_color='blue', legend_label='Close')
      
      #hover = HoverTool()
      #hover.tooltips = """
      #<div style=padding=5px>DATE:@sdate</div>
      #<div style=padding=5px>OPEN:@open</div>
      #"""
      #plot.add_tools(hover)
      #show(plot) 
      plot.add_tools(HoverTool(show_arrow=False,tooltips=[("DATE", "@sdate"), ("OPEN", "@open"), ("CLOSE", "@close")]))
      save(plot)
      '''
      #return render_template(dst['stocks']+'.html')
      return render_template('stocks.html')
  except Exception as e:
      flash(e)
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
  app.run(port=33507)
  #app.run(debug='True')
'''
'''      
