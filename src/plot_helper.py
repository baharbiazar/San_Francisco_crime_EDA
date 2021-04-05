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


def plot_violent_years(df18 , df19, df20):

    '''
    returns a bar plot comparing violent crime counts 
    '''

    viol_cat_18=df18.groupby('Incident Category').count().sort_values(by='Row ID').reset_index(drop= False)
    viol_cat_19=df19.groupby('Incident Category').count().sort_values(by='Row ID').reset_index(drop= False)
    viol_cat_20=df20.groupby('Incident Category').count().sort_values(by='Row ID').reset_index(drop= False)


    fig , ax = plt.subplots(figsize=(10,6))  

    x= np.arange(7)

    u= viol_cat_18['Row ID']
    v= viol_cat_19['Row ID']
    w= viol_cat_20['Row ID']


    ax.bar(x+0.2 ,w, width= 0.2 , label = '2020')
    ax.bar(x,v, width= 0.2, label = '2019')
    ax.bar(x-0.2, u , width = 0.2 , label = '2018')

    ax.set_xticks(x)
    ax.set_xticklabels(viol_cat_20['Incident Category'], rotation =90)
    plt.title('SF Violent Crime Counts: Mar-Dec')
    plt.legend()
    plt.xticks(fontsize  = 13)

    plt.savefig('../images/viol_comp.png', dpi=80, bbox_inches='tight')

    return ax




def plot_prop_years(df18 , df19, df20):
    
    '''
    returns a bar plot comparing porperty crime counts 
    '''

    prop_cat_18=df18.groupby('Incident Category').count().sort_values(by='Row ID').reset_index(drop= False)
    prop_cat_19=df19.groupby('Incident Category').count().sort_values(by='Row ID').reset_index(drop= False)
    prop_cat_20=df20.groupby('Incident Category').count().sort_values(by='Row ID').reset_index(drop= False)


    fig , ax = plt.subplots(figsize=(10,6))  

    x= np.arange(4)

    p= prop_cat_18['Row ID']
    q= prop_cat_19['Row ID']
    r= prop_cat_20['Row ID']


    ax.bar(x+0.1 ,r, width= 0.1 , label = '2020')
    ax.bar(x,q, width= 0.1, label = '2019')
    ax.bar(x-0.1, p , width = 0.1 , label = '2018')

    ax.set_xticks(x)
    ax.set_xticklabels(prop_cat_20['Incident Category'], rotation =90)

    plt.title('SF Property Crime Counts: Mar-Dec')
    plt.xticks(fontsize  = 13)
    plt.legend()

    plt.savefig('../images/property_comp.png', dpi=80, bbox_inches='tight')

    return ax


def plot_viol_subcats(df19 , df20):

    '''
    returns a plot with violent sub categories, showing 2020 growth rate 
    '''

    viol_sub_19 = df19.groupby(['Incident Category', 'Incident Subcategory']).count().sort_values(by=['Incident Category','Row ID'], ascending = False).reset_index()
    viol_sub_20 = df20.groupby(['Incident Category', 'Incident Subcategory']).count().sort_values(by=['Incident Category','Row ID'], ascending = False).reset_index()

    leftv= viol_sub_19[['Incident Category' , 'Incident Subcategory' , 'Row ID']]
    leftv.rename(columns={'Row ID' : '2019 Count'} , inplace= True)


    rightv = viol_sub_20[['Incident Category' , 'Incident Subcategory' , 'Row ID']]
    rightv.rename(columns={'Row ID' : '2020 Count'} , inplace= True)

    compare_viol = pd.merge(leftv, rightv, how = 'left', on =['Incident Category' , 'Incident Subcategory'])

    compare_viol['growth'] = round((((compare_viol['2020 Count'] - compare_viol['2019 Count'])*100)/ compare_viol['2019 Count']), 2)

    
    
    fig , ax = plt.subplots(figsize= (12,10))

    plt.barh(compare_viol['Incident Subcategory'] , compare_viol['growth'] ,color=(compare_viol['growth'] > 0).map({True: 'r',
                                                        False: 'b'}), edgecolor= None)

    plt.title('SF Violent Crime Change: 2019-2020 , Mar-Dec')

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
        
    plt.yticks(fontsize=14)
    #ax.axes.get_xaxis().set_visible(False)
    ax.tick_params(axis="y", left=False)


    for p in ax.patches:
        width = p.get_width()
        height = p.get_height()
        x, y = p.get_xy() 
        if width>0:
            ax.annotate(f'{width}%', (x + width+ 1
                                    , y+ height/2.5))
            
        else:
            ax.annotate(f'{width}%', (x + width -22 , y+ height/2.5))

    plt.savefig('../images/sub_viol.png', dpi=80, bbox_inches='tight')
    return ax
        
        


def plot_prop_subcats(df19 , df20):

    '''
    returns a plot with violent sub categories, showing 2020 growth rate 
    '''

    prop_sub_19 = df19.groupby(['Incident Category', 'Incident Subcategory']).count().sort_values(by=['Incident Category','Row ID'], ascending = False).reset_index()
    prop_sub_20 = df20.groupby(['Incident Category', 'Incident Subcategory']).count().sort_values(by=['Incident Category','Row ID'], ascending = False).reset_index()

    leftp= prop_sub_19[['Incident Category' , 'Incident Subcategory' , 'Row ID']]
    leftp.rename(columns={'Row ID' : '2019 Count'} , inplace= True)


    rightp = prop_sub_20[['Incident Category' , 'Incident Subcategory' , 'Row ID']]
    rightp.rename(columns={'Row ID' : '2020 Count'} , inplace= True)

    compare_prop = pd.merge(leftp, rightp, how = 'left', on =['Incident Category' , 'Incident Subcategory'])

    compare_prop['growth'] = round((((compare_prop['2020 Count'] - compare_prop['2019 Count'])*100)/ compare_prop['2019 Count']), 2)

    
    
    fig , ax = plt.subplots(figsize= (12,10))

    plt.barh(compare_prop['Incident Subcategory'] , compare_prop['growth'] ,color=(compare_prop['growth'] > 0).map({True: 'r',
                                                        False: 'b'}), edgecolor= None)

    plt.title('SF Property Crime Change: 2019-2020 , Mar-Dec')

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
        
    plt.yticks(fontsize=14)
    #ax.axes.get_xaxis().set_visible(False)
    ax.tick_params(axis="y", left=False)


    for p in ax.patches:
        width = p.get_width()
        height = p.get_height()
        x, y = p.get_xy() 
        if width>0:
            ax.annotate(f'{width}%', (x + width+ 1
                                    , y+ height/2.5))
            
        else:
            ax.annotate(f'{width}%', (x + width -22 , y+ height/2.5))

    plt.savefig('../images/sub_prop.png', dpi=80, bbox_inches='tight')

    return ax





























        



