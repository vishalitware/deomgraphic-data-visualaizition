
# coding: utf-8

# In[2]:


import  numpy as np 
import  matplotlib . pyplot as plt 
import  pandas as pd 


# In[5]:


#Demographic data 


# In[10]:


import os


# In[24]:


os . chdir('E:\\Datasets\\')


# In[27]:


data = pd.read_csv('DemographicData.csv')
data


# In[29]:


data.head()


# In[33]:


data.tail()


# In[36]:


data[2:3]


# In[38]:


data[:10]


# In[56]:


data[:5]


# In[2]:


import numpy as np
import pandas as pd
from scipy import stats
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
import datetime
import json
from bs4 import BeautifulSoup
import requests
import time

def fetchCryptoClose(fsym, tsym):
    # function fetches the close-price time-series from cryptocompare.com
    # it may ignore USDT coin (due to near-zero pricing)
    # daily sampled
    cols = ['date', 'timestamp', fsym]
    lst = ['time', 'open', 'high', 'low', 'close']
    timestamp_today = datetime.today().timestamp()
    curr_timestamp = timestamp_today

    for j in range(2):
        df = pd.DataFrame(columns=cols)
        url = "https://min-api.cryptocompare.com/data/histoday?fsym=" + fsym +               "&tsym=" + tsym + "&toTs=" + str(int(curr_timestamp)) + "&limit=3"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        dic = json.loads(soup.prettify())
        for i in range(1, 4):
            tmp = []
            for e in enumerate(lst):
                x = e[0]
                y = dic['Data'][i][e[1]]
                if(x == 0):
                    tmp.append(str(timestamp2date(y)))
                tmp.append(y)
            if(np.sum(tmp[-4::]) > 0):  # remove for USDT
                tmp = np.array(tmp)
                tmp = tmp[[0,1,4]]  # filter solely for close prices
                df.loc[len(df)] = np.array(tmp)
        # ensure a correct date format
        df.index = pd.to_datetime(df.date, format="%Y-%m-%d")
        df.drop('date', axis=1, inplace=True)
        curr_timestamp = int(df.ix[0][0])
        if(j == 0):
            df0 = df.copy()
        else:
            data = pd.concat([df, df0], axis=0)
    data.drop("timestamp", axis=1, inplace=True)

    return data  # DataFrame

# N-Cryptocurrency Portfolio (tickers)
fsym = ['BTC', 'ETH', 'XRP', 'LTC', 'DASH', 'XMR', 'ETC', 'MAID', 'XEM', 'REP']
# vs. 
tsym = 'USD'

for e in enumerate(fsym):
    print(e[0], e[1])
    if(e[0] == 0):
        try:
            data = fetchCryptoClose(e[1], tsym)
        except:
            pass
    else:
        try:
            data = data.join(fetchCryptoClose(e[1], tsym))
        except:
            pass

# ensure values to be floats

# save portfolio to a file (HDF5 file format)
store = pd.HDFStore('portfolio2.h5')
store['data'] = data
store.close()

# read in your portfolio from a file
df = pd.read_hdf('portfolio2.h5', 'data')
print(df)

