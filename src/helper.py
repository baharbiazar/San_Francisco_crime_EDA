import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
plt.style.use('ggplot')
import matplotlib.ticker as tick

import geopandas as gpd
import descartes
from shapely.geometry import Point , Polygon

import folium
from folium import plugins
import json


def extract_df(df , cols):
    '''
    makes a copy of the original df
    drops the columns we don't want
 

    ARGS:
    df = original pandas dataframe
    cols = list of column names to DROP

    Return:
    extract_df

    '''
    extract_df= df.drop(cols, axis=1)

    return extract_df

def to_datetime(df, date_col, time_col):
    '''
    converts string values of date col and time col to a datetime format

    ARGS:
    df = dataframe
    date_col = date column , string
    time_col = time column , string

    Returns:
    df
    '''
    df[date_col] = pd.to_datetime(df[date_col])
    df[time_col] = pd.to_datetime(df[time_col] , format = '%H:%M')

    return df

def plot_crime_per_year(df,years, year_col):

    '''
    plots a histogram of all crime counts in the given years

    ARGS:
    df = dataframe
    years = list of years, years are integers
    year_col = name of the column that has year values, string

    Returns:
    a histogram

    '''
    x= []
    y= []

    for i in years:

        i_df= df[df[year_col] == i].reset_index(drop = True)
        y.append(i_df.count()[0])
        x.append(str(i))
        


    fig , ax = plt.subplots(dpi= 100)

    ax.bar(x,y , color = 'slategrey')
    plt.title('SF Total Crime Count')
    #plt.ylabel('Crime Count')
    plt.ylim()
    ax.yaxis.set_major_locator(tick.MultipleLocator(80000))

    
    for p in ax.patches:
        height = p.get_height()
        width = p.get_width()
        x, y = p.get_xy() 
        ax.annotate(f'{height}', (x+ width/4 , y+ height+3))

    plt.savefig('../images/total_counts.png', dpi=80, bbox_inches='tight')

    return ax



def crime_per_year(df, year , year_col):
    
    '''
    returns a df of crimes that only happened in the year passed

    ARGS:
    df= dataframe
    year = integer year
    year_col = the column that has the years stored, string
    
    Returns dataframe
    '''
    df_year = df[df[year_col] == year].reset_index(drop = True )
    return df_year
    
def violent_(df):
    '''
    returns a df with only violent crime categories 
    '''

    violent = df[(df['Incident Category'] == 'Homicide')
                |(df['Incident Category'] == 'Rape')
                |(df['Incident Category'] == 'Robbery')
                |(df['Incident Category'] == 'Assault')
                |(df['Incident Category'] == 'Traffic Violation Arrest')
                |(df['Incident Category'] == 'Offences Against The Family And Children')
                |(df['Incident Category'] == 'Drug Offense')].reset_index(drop= True)

    return violent

def property_(df):
    '''
    returns a df with only property crime categories 
    '''


    property_= df[(df['Incident Category'] == 'Burglary')
                |(df['Incident Category'] == 'Motor Vehicle Theft')
                |(df['Incident Category'] == 'Larceny Theft')
                |(df['Incident Category'] == 'Arson')].reset_index(drop= True)

    return property_

def property_after_date(df , year, month):

    '''
    returns a df with property crimes in a certain year, 
    after a certain month

    df = dataframe
    year = int
    month = int
    '''

    p = df[(df['Incident Year'] == year) & (df['Incident Date'].dt.month > month)].reset_index(drop=True)


    return p


def violent_after_date(df , year, month):

    '''
    returns a df with violent crimes in a certain year, 
    after a certain month

    df = dataframe
    year = int
    month = int
    '''

    p = df[(df['Incident Year'] == year) & (df['Incident Date'].dt.month > month)].reset_index(drop=True)


    return p


    



    


    
    

    


  



