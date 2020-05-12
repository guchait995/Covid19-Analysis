import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy
from pmdarima import auto_arima
from datetime import timedelta
# from pandas.io.json import json_normalize
BASE_URL="https://api.covid19india.org"
NATIONAL_DATA_URL="{}/data.json".format(BASE_URL)
def fetch_data(url):
    response=requests.get(url)
    if(response.status_code==200): 
        return response.json()
    return {}

def create_dataframe(json):
    df=pd.json_normalize(json)
    df["date"]="2020,"+df["date"]
    df['date']=pd.to_datetime(df["date"],format="%Y,%d %B ")
    df.set_index('date',inplace=True)
    return df


def plot_graph(title,df,ax):
    if ax == None:
        ax=df.plot(title=title,figsize=(10,7),fontsize=20)
    else:
        df.plot(title=title,figsize=(10,7),fontsize=20,ax=ax)
    return ax     

def plot_graph_bar(title,df):
    print(df)
    # [row, col] = numpy.where(df==numpy.max(df))
    df.plot(title=title,figsize=(10,7),fontsize=20).bar(x=df.index,height=df)
    plt.plot()
   
    
def test_train_split(df,test_length=7):
        train=df[:len(df)-test_length]
        test=df[len(df)-test_length: len(df)]
        return test,train
    
def find_arima(df):
    print(df)
    model=auto_arima(df,m=1)
    return model

def forcast(train_df,test_df,test_length=7):
    model=find_arima(train_df)
    model.fit(train_df)
    df=model.predict(n_periods=test_length)
    forecast_df = pd.DataFrame(df,index = test_df.index,columns=['Prediction on the Test Set'])
    return forecast_df

def forcastFuture(full_df,test_length=7):
    model=find_arima(full_df)
    model.fit(full_df)
    df=model.predict(n_periods=test_length)
    start_date = full_df.index[-1]
    print(start_date)
    days = pd.date_range(start_date+timedelta(1), start_date + timedelta(test_length), freq='D')
    forecast_df = pd.DataFrame(df,index = days,columns=["Forcast Future 7 Days: [{}-{}]".format(start_date.strftime("%d/%m/%Y")
,(start_date + timedelta(test_length)).strftime("%d/%m/%Y"))])
    return forecast_df


def init():
    data=fetch_data(NATIONAL_DATA_URL)
    cases_time_series=data["cases_time_series"]
    df=create_dataframe(cases_time_series)
    df["totalconfirmed"]=df["totalconfirmed"].astype(int)
    test_df,train_df=test_train_split(df["totalconfirmed"])
    forcast_df=forcast(train_df,test_df)
    start_date = df.index[-1]
    forcast_future_df=forcastFuture(df["totalconfirmed"])
    
    ax=plot_graph("",train_df,None)
    ax=plot_graph("",test_df,ax)
    ax=plot_graph("",forcast_df,ax)
    ax=plot_graph("Covid 19 Future Stats:-".format(start_date),forcast_future_df,ax)
    
    plt.plot()
    plt.show() 
    # plot_graph_bar(title="Covid-19 : Total Confirmed Cases", df=df["totalconfirmed"])
    print(df)    
    
init()    