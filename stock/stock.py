
# coding: utf-8

# In[57]:


import pandas as pd
from pandas_datareader import data, wb
import datetime
import time


# In[66]:


def get_stock_pdf(ticker):
    start = datetime.datetime(2018, 1, 1)
    end = datetime.date.today()
    print(ticker)
    time.sleep(1)
    return ticker, data.DataReader(ticker, "iex", start, end)


# In[49]:


def read_stock_data(file):
    with open(file, 'r') as f:
        fl = f.readlines()
        tickers = list(filter(lambda x: x, map(lambda x: x.split(',')[1].strip(), fl)))
        tickers_map = {i.split(',')[1].strip(): i.split(',')[0].split(' ') for i in fl}
        return tickers, tickers_map


# In[50]:


def output_csv(pdfs):
    for pdf in pdfs:
        pdf[1].to_csv('data/'+pdf[0]+'.csv', sep=',', encoding='utf-8')
        


# In[54]:


tickers, tickers_map = read_stock_data('ticker_list')
print(tickers)


# In[69]:


pdfs = [get_stock_pdf(t) for t in tickers]


# In[70]:


output_csv(pdfs)

