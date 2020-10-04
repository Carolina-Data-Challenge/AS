#!/usr/bin/env python
# coding: utf-8

# In[185]:


# CDC project 


# In[382]:


get_ipython().run_line_magic('matplotlib', 'notebook')
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
from datetime import datetime

# US, San-Francisco. How wildfire affects air quality. 

data = pd.read_csv('OpenAQSanFran.csv', usecols=[0,3,5,6,7])

# I use two locations to get values of four parameters which reflect the AQ. Redwood City gives pm25, o3 (Ozone), and
# co (Carbon Monoxide), while Laney College gives bc (black carbon). The measurements are provided for the period
# from 2020-07-03 to 2020-09-15.

df1 = data[data['location']=='Redwood City']
df1 = df1[(df1['parameter']=='pm25') | (df1['parameter']=='o3') | (df1['parameter']=='co')]
df2 = data[data['location']=='Laney College']
df2 = df2[df2['parameter']=='bc']
frames = [df1, df2]
df = pd.concat(frames)


df['utc'] = pd.to_datetime(df['utc'])
df.sort_values(by='utc', inplace=True)
df.drop(columns=['location'], axis=1, inplace=True)
df['month_date'] = df['utc'].dt.strftime('%m-%d')
df['time'] = df['utc'].dt.time
df.reset_index(inplace=True)
#df.drop(columns=['index', 'utc'], inplace=True)
df = df[['month_date', 'time', 'parameter', 'value', 'unit']]

df.head(20)


# In[388]:


df_pm25 = df[df['parameter']=='pm25']
df_o3 = df[df['parameter']=='o3']
df_co = df[df['parameter']=='co']
df_bc = df[df['parameter']=='bc']

df_pm25 = df_pm25.groupby('month_date').agg({'value': np.mean})
df_pm25.rename(columns={'value':'pm25'}, inplace=True)

df_o3 = df_o3.groupby('month_date').agg({'value': np.mean})
df_o3.rename(columns={'value':'o3'}, inplace=True)

df_co = df_co.groupby('month_date').agg({'value': np.mean})
df_co.rename(columns={'value':'co'}, inplace=True)

df_bc = df_bc.groupby('month_date').agg({'value': np.mean})
df_bc.rename(columns={'value':'bc'}, inplace=True)

df_param = df_pm25.join(df_o3).join(df_co).join(df_bc)

pm25 = np.array(df_param['pm25'])
o3 = np.array(df_param['o3'])
co = np.array(df_param['co'])
bc = np.array(df_param['bc'])

#df_param['month_date'] = df_param.index
days = np.array(df_param.index)
days5 = days[::5]

#df_param['month'] = pd.to_datetime(df_param['date']).dt.month
#df_param['day'] = pd.to_datetime(df_param['date']).dt.day

#df_param['month_date'] = df_param['month_date'].dt.strftime('%m-%d')

df_param


# In[ ]:





# In[410]:


def picture():
        
    fig = plt.figure(figsize=(8,14))
    ttl = fig.suptitle('Air Quality in San-Francisco, July-September 2020', fontsize=16, x=0.53, y=0.99) 
    pos = np.arange(0, 73, step=5)
  
    ax1 = fig.add_subplot(411)
    ax1.plot(pm25, '-b', linewidth=1.5, markersize=1, alpha = 1)
    ax1.title.set_text('PM2.5')
    ax1.set(ylabel='$\mu g/m^3$')
    plt.xticks(pos, days5, alpha=0.8, rotation='50')
    plt.gca().fill_between(range(73), 0, 50, facecolor='green', alpha=0.1)
    plt.gca().fill_between(range(73), 50, 100, facecolor='yellow', alpha=0.1)
    plt.gca().fill_between(range(73), 100, 145, facecolor='orange', alpha=0.1)
    plt.text(1, 40, 'good')
    plt.text(1, 90, 'moderate')
    plt.text(1, 135, 'unhealthy')
    
    ax2 = fig.add_subplot(412)
    ax2.plot(bc, '-b', linewidth=1.5, markersize=1, alpha = 1)
    ax2.title.set_text('BC (black carbon)')
    ax2.set(ylabel='$\mu g/m^3$')
    plt.xticks(pos, days5, alpha=0.8, rotation='50')
    
    ax3 = fig.add_subplot(413)
    ax3.plot(co, '-b', linewidth=1.5, markersize=1, alpha = 1)
    ax3.title.set_text('CO (carbon monoxide)')
    ax3.set(ylabel='$ppm$')
    plt.xticks(pos, days5, alpha=0.8, rotation='50')
    
    ax4 = fig.add_subplot(414)
    ax4.plot(o3, '-b', linewidth=1.5, markersize=1, alpha = 1)
    ax4.title.set_text('O3 (ozone)')
    ax4.set(ylabel='$ppm$')
    plt.xticks(pos, days5, alpha=0.8, rotation='50')
    
    fig.tight_layout(pad = 3)
    
    return 

picture()


# In[ ]:


# Analyzing graphs, we see that in September all the parameters of AQ has grown in San-Francisco due to wildfires.
# Black carbon and Carbon monoxide seem to be on levels higher than before the wildfires started, while the level 
# of O3 fluctuated significantly, with regular values on 9-08 - 9-10.


# In[ ]:




