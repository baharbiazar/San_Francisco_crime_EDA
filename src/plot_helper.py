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


def plot_crime_by_month(df , date_col):
    '''
    graphs a line plot for each year based on crime counts per month

    ARGS: 
    df = dataframe
    years_list = list of years, int

    Returns a plot

    '''

    grouped = df.groupby([df[date_col].dt.year, df[date_col].dt.month]).count()

    fig , ax = plt.subplots(figsize = (12, 6 ))

    x= ['Jan' , 'Feb' , 'Mar', 'Apr' , 'May' , 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    m= grouped.iloc[:12, 2]
    n= grouped.iloc[12:24, 2]
    o= grouped.iloc[24:36, 2]

    ax.plot(x , m , label = '2018' , color = 'b')
    ax.scatter(x,m, color = 'b')
    ax.plot(x , n , label = '2019', color= 'g')
    ax.scatter(x,n, color = 'g')
    ax.plot(x , o , label= '2020', color = 'coral')
    ax.scatter(x,o, color = 'coral')
    plt.title('SF Monthly Crime Counts')
    plt.legend()

    plt.savefig('../images/monthly.png', dpi=80, bbox_inches='tight')
    
    return ax


def plot_cats_per_year(df , date_col, cat_col):

    '''
    returns 3 subplots for year 2018, 2019, 2020
    each subplot showing the most occuring crimes

    ARGS:
    df = dataframe
    date_col = name of column dates , string
    cat_col = name of category column, string
    '''



    df_2020_cat= df[df[date_col].dt.year ==2020].groupby(cat_col).count().sort_values(by = 'Row ID', ascending = True).reset_index()
    df_2019_cat= df[df[date_col].dt.year ==2019].groupby(cat_col).count().sort_values(by = 'Row ID', ascending = True).reset_index()
    df_2018_cat= df[df[date_col].dt.year ==2018].groupby(cat_col).count().sort_values(by = 'Row ID', ascending = True).reset_index()

    

    
    a= df_2018_cat[cat_col][36:]
    b= df_2018_cat['Row ID'][36:]

    c= df_2019_cat[cat_col][36:]
    d= df_2019_cat['Row ID'][36:]

    e= df_2020_cat[cat_col][36:]
    f= df_2020_cat['Row ID'][36:]



    fig , axs = plt.subplots (3,1, figsize = (12, 18))
    #fig.tight_layout()

    axs[0].barh(a,b)
    axs[0].set_title('SF Crime Count per Category, 2018')

    axs[1].barh(c,d)
    axs[1].set_title('SF Crime Count per Category, 2019')

    axs[2].barh(e,f)
    axs[2].set_title('SF Crime Count per Category, 2020')
    axs[2].set_xlim(0, 51000)

    plt.savefig('../images/cat_per_year.png', dpi=80, bbox_inches='tight')

    return axs
















    



