import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy
from pmdarima import auto_arima
from datetime import timedelta
import sys
import argparse, sys
BASE_URL="https://api.covid19india.org"
NATIONAL_DATA_URL="{}/data.json".format(BASE_URL)
COLUMN_HELP_TEXT='Pass Column on which you want to forcast - Options:[ totalconfirmed | totaldeceased | totalrecovered | active | all]'
DAYS_HELP_TEXT='Pass number of days you want to forcast Integer(Days)'
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


def plot_graph(title,df,ax=None):
    if ax == None:
        ax=df.plot(title=title,figsize=(10,7),fontsize=20)
    else:
        df.plot(title=title,figsize=(10,7),fontsize=20,ax=ax)
    return ax     

def plot_graph_bar(title,df,ax=None):
    if ax == None:
        ax=df.plot(title=title,figsize=(10,7),fontsize=20).bar(x=df.index,height=df)
    else:
        df.plot(title=title,figsize=(10,7),fontsize=20,ax=ax).bar(x=df.index,height=df)
    return ax 
    
    
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

def forcastFuture(full_df,test_length=7,name=""):
    model=find_arima(full_df)
    model.fit(full_df)
    df=model.predict(n_periods=test_length)
    start_date = full_df.index[-1]
    print(start_date)
    days = pd.date_range(start_date+timedelta(1), start_date + timedelta(test_length), freq='D')
    forecast_df = pd.DataFrame(df,index = days,columns=["Forcast Future 7 Days ({}): [{}-{}]".format(name,start_date.strftime("%d/%m/%Y")
,(start_date + timedelta(test_length)).strftime("%d/%m/%Y"))])
    return forecast_df

def parse_arguments():
    parser=argparse.ArgumentParser()
    parser.add_argument('--days', help=DAYS_HELP_TEXT,default=7)
    parser.add_argument('--column', help=COLUMN_HELP_TEXT,default="totalconfirmed")
    
    args=parser.parse_args()
    d=vars(args)
    return d
    
def init():
    data=fetch_data(NATIONAL_DATA_URL)
    cases_time_series=data["cases_time_series"]
    df=create_dataframe(cases_time_series)
    df["totalconfirmed"]=df["totalconfirmed"].astype(int)
    df["totaldeceased"]=df["totaldeceased"].astype(int)
    df["totalrecovered"]=df["totalrecovered"].astype(int)
    df["active"]=df["totalconfirmed"]-df["totaldeceased"]-df["totalrecovered"]
    args=parse_arguments()
    forcast_days=int(args['days'])
    action=args['column']    
    # test_df,train_df=test_train_split(df[action])
    # forcast_df=forcast(train_df,test_df)
    # start_date = df.index[-1]
    
    
    ax=plot_graph("",df,None)
    
    if action == "all":
        forcast_future_df=forcastFuture(df["totalconfirmed"],forcast_days,"totalconfirmed")
        plot_graph("Covid 19 Future Stats:- ({})".format("totalconfirmed"),forcast_future_df,ax)
        forcast_future_df=forcastFuture(df["totaldeceased"],forcast_days,"totaldeceased")
        plot_graph("Covid 19 Future Stats:- ({})".format("totaldeceased"),forcast_future_df,ax)
        forcast_future_df=forcastFuture(df["totalrecovered"],forcast_days,"totalrecovered")
        plot_graph("Covid 19 Future Stats:- ({})".format("totalrecovered"),forcast_future_df,ax)
        forcast_future_df=forcastFuture(df["active"],forcast_days,"active")
        plot_graph("Covid 19 Future Stats:- ({})".format("active"),forcast_future_df,ax)
    
    else:
        forcast_future_df=forcastFuture(df[action],forcast_days,action)    
        plot_graph("Covid 19 Future Stats:- ({})".format(action),forcast_future_df,ax)
    
    plt.plot()
    plt.show()  
    

   
if __name__ == "__main__":
    init()