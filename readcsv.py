import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
#from scipy import stats
import sqlite3

conn=sqlite3.connect('Companylist.db')
c = conn.cursor()
c.execute('''CREATE TABLE NASDAQ
             ([generated_id] INTEGER PRIMARY KEY,[Symbol] text, [Name] text, [Sector] text)''')
c.execute('''CREATE TABLE AMEX
             ([generated_id] INTEGER PRIMARY KEY,[Symbol] text, [Name] text, [Sector] text)''')
c.execute('''CREATE TABLE NYSE
             ([generated_id] INTEGER PRIMARY KEY,[Symbol] text, [Name] text, [Sector] text)''')
conn.commit()
df1 = pd.read_csv('NASDAQlist.csv')
dflist1=df1[['Symbol','Name','Sector']]
dflist1.to_sql('NASDAQ', conn, if_exists='append', index = False) # Insert the values from the csv file into the table 'CLIENTS' 
df2 = pd.read_csv('AMEXlist.csv')
dflist2=df2[['Symbol','Name','Sector']]
dflist2.to_sql('AMEX', conn, if_exists='append', index = False) # Insert the values from the csv file into the table 'CLIENTS' 
df3 = pd.read_csv('NYSElist.csv')
dflist3=df3[['Symbol','Name','Sector']]
dflist3.to_sql('NYSE', conn, if_exists='append', index = False) # Insert the values from the csv file into the table 'CLIENTS' 
c.execute('''
SELECT Name
FROM NYSE''')
print(c.fetchall())
#print(dflist)