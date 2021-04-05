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

    plt.savefig('../images/total_counts.png', dpi=300, bbox_inches='tight')

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
    
def plot_crime_count_monthly(df):
    pass


    


    
    

    


  



