#If you are not using Jupiter notebook for opening this file Uncomment plt.show() line to see graphs
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import requests
import seaborn as sns
import urllib.request
from bs4 import BeautifulSoup
import datetime
import calendar

# DataFrame
df_Orders = pd.read_csv('order_2020-08-11_Harbor-sales2.csv', delimiter=';')
df_Clearance = pd.read_csv('product_2020-08-11_Harbor-Clearance2.csv', delimiter=';')
df_TopDeals = pd.read_csv('product_2020-08-11_Harbor-Top_Deals2.csv', delimiter=';')

# TEST
print(df_Orders.head())
print(df_Orders.columns)
# print(df_Clearance.head())
# print(df_Clearance.columns)
# print(df_TopDeals.head())
# print(df_TopDeals.columns)

# Add Month
df_Orders['Month'] = df_Orders['Date'].str[5:7]
# print(df_Orders['Month'])

# Find empty values in Dataframe (remove if any)
# nan_df = df_Orders[df_Orders.isna().any(axis=1)]
# print(nan_df.head())

# Add Week day
def findDay(dates):
    lits = []
    for date in dates:
        date= str(date).replace('-',' ')
        print(date)
        bought = datetime.datetime.strptime(date, '%Y %m %d').weekday()
        lits.append(calendar.day_name[bought])
    return lits
df_Orders['Week'] = findDay(df_Orders['Date'].str[0:10])

# Add day
df_Orders['Day'] = df_Orders['Date'].str[8:10]

# Add day time
df_Orders['Time'] = 'Evening'
df_Orders.loc[(df_Orders['Date'].str[11:13]>='00') & (df_Orders['Date'].str[11:13]<'06'),'Time'] = 'Night'
df_Orders.loc[(df_Orders['Date'].str[11:13]>='06') & (df_Orders['Date'].str[11:13]<'12'),'Time'] = 'Morning'
df_Orders.loc[(df_Orders['Date'].str[11:13]>='12') & (df_Orders['Date'].str[11:13]<'18'),'Time'] = 'Afternoon'

# Sales
df_Orders['Sales'] = df_Orders['Total'].str[1:].astype(float)
df_Orders.loc[(df_Orders['Status'] != 'Payment accepted') &
              (df_Orders['Status'] != 'On backorder (paid)') &
               (df_Orders['Status'] != 'Processing in progress'), 'Sales'] = 0.0
print(df_Orders['Sales'].iloc[70:76])

# Best Month
results = df_Orders.groupby('Month').sum()
months = range(1, 9)
print(results['Sales'])
#plt.bar(months, results['Sales'])
#plt.show()

#Compare to CoronaVirus
results = df_Orders.groupby('Month').sum()
months = [
'April',
'May',
'June',
'July',
'August']
#print(results['Sales'])
resultspercent = [ 73.4,-18.9, -12.18, 136.9, -62.3]
coronadatapercent = [95.4,16.8,-15.9,59.4,67]
plt.plot(months,coronadatapercent, color='orange')
salesbar=plt.bar(months, resultspercent, color='green')
salesbar[1].set_color('r')
salesbar[2].set_color('r')
salesbar[4].set_color('r')
plt.show()

#Best week
results = df_Orders.groupby('Week').sum()
weeks = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
print(results['Sales'])
#plt.bar(weeks, results['Sales'])
#plt.show()

# Everything else is done with seaborn by changing arguments of catplot
sns.set()
#sns.countplot('Customer', data=df_Orders)
sns.catplot(x='Day',y='Sales', data=df_Orders, kind="point", hue='Time', ci=False)
#plt.show()
#plt.xticks(months)

df_Price1 = df_TopDeals.drop(['Product ID','Image','Name','Reference','Category','Quantity','Status','Position'],axis=1)
sns.boxplot(data=df_Price1)

plt.ylim(-100, 9800)
#plt.show()
df_Price2 = df_Clearance.drop(['Product ID','Image','Name','Reference','Category','Quantity','Status','Position'],axis=1)
sns.boxplot(data=df_Price2)
plt.ylim(-100, 9800)
#plt.show()

#Download images
"""
#test = "test0"

#For Clearance Images

Images = list(df_Clearance['Image'])
Names = list(df_Clearance['Name'])

for i in range(len(Images)):
     try:
         urllib.request.urlretrieve(str(Images[i]),
                           "D:\work\DS\python\images\{}.jpg".format(str(Names[i])))
     except:
         pass

#For Top Deals Images

Images = list(df_TopDeals['Image'])
Names = list((df_TopDeals['Name']))

for i in range(len(Images)):
     try:
         urllib.request.urlretrieve(str(Images[i]),
                           "D:\work\DS\python\images\{}.jpg".format(str(Names[i])))
     except:
         pass
"""

# Scares at store
sns.set()
#sns.countplot('Customer', data=df_Orders)
"""
df_TopDeals= df_TopDeals.sort_values(by=['Quantity'])
print(len(df_TopDeals))
df_TopDeals= df_TopDeals.drop(columns=['Product ID','Image','Reference','Category','Price (tax excl.)','Price (tax incl.)',
                          'Status','Position'])
print(df_TopDeals.head(90))
"""

# sns.catplot(x='Name', y='Quantity', data=df_TopDeals, kind='bar')
#plt.bar(months, results['Sales'])
#plt.xticks(months)
#plt.show()