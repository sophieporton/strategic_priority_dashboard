# %%
#import required packages

import streamlit as st 
import plotly.express as px
import pandas as pd
import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource
from bokeh.palettes import Viridis3
from bokeh.models import HoverTool

# %%
#define function to plot oas by ward

def plot_wards(df, column='', string='', agg='',title=''):
    df=df[df.MEASURES_NAME== 'Percent']
    df=df[df[column].str.contains(string)==True]
    fig = px.choropleth(df.dissolve(by='ward_name', aggfunc ={'OBS_VALUE':agg}),
                   geojson=df.dissolve(by='ward_name', aggfunc ={'OBS_VALUE':agg}).geometry,
                   locations=df.dissolve(by='ward_name',aggfunc ={'OBS_VALUE':agg}).index,
                   color="OBS_VALUE",
                   color_continuous_scale = 'viridis_r',
                   projection="mercator",
                   hover_name=df.dissolve(by='ward_name',aggfunc ={'OBS_VALUE':agg}).index )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(coloraxis_colorbar=dict(title=title))
    fig.update_traces(hovertemplate='Ward name: <b>%{location}</b> <br>Percentage: <b>%{z:.2f}%</b>')
    st.plotly_chart(fig,use_container_width = True)

# %%
#define function to merge spatial data with variable data

def merge_spatial_data(gdf, df, left_on="", right_on=""):
    gdf=gdf.merge(df, left_on=left_on, right_on=right_on)
    return gdf

# %%
#read in aggregated oa by ward dataset from main python file 

#merged_wd_oa = st.session_state['merged_wd_oa']

# %%
#read in deprivation by oa dataset

try:
  deprivation_oa = pd.read_csv('lbth_census_2021_deprivation_oa.csv')
except:
  deprivation_oa = pd.read_csv('https://www.nomisweb.co.uk/api/v01/dataset/NM_2031_1.data.csv?date=latest&geography=629165479...629165982,629303674...629303812,629317322...629317326,629317336...629317343,629317349...629317360,629317362...629317366,629317371,629317374,629317376,629317378,629317379,629317381,629317385,629317388...629317392,629317394...629317397,629317399...629317403,629317405...629317407,629317409,629317411,629317412,629317416...629317420,629317422...629317424,629317426,629317429...629317434,629317436,629317437,629317440...629317442,629317444...629317450,629317452...629317456,629317459...629317461,629317463,629317466...629317468,629317472,629317474...629317479,629317481,629317483,629317486,629317487,629317490,629317492,629317494,629317495,629317497,629317499...629317502,629317504,629317505,629317507...629317509,629317512...629317514,629317517,629317520,629317523,629317525,629317527,629317531,629317534,629317535,629317537,629317538,629317540,629317543...629317548,629317551,629317554,629317555,629317558,629317560,629317562,629317563,629317565,629317566,629317569...629317573,629317576...629317578,629317580,629317582,629317584,629317585,629317587,629317590...629317592,629317594,629317596...629317599,629317601,629317603,629317604,629317606,629317607,629317610,629317612,629317613,629317615...629317617,629317619...629317621,629317623,629317625...629317629,629317631...629317634,629317636,629317640,629317648,629317650...629317659,629317662,629317663,629317666...629317669,629317672...629317687,629317689,629317691,629317694,629317695,629317697,629317698,629317700,629317701,629317703,629317704,629317706,629317707,629317711...629317714,629317716,629317718...629317720,629317722...629317724,629317726,629317729,629317731,629317733,629317736...629317742,629317744,629317746...629317748,629323624,629323625&c2021_dep_6=1...5&measures=20301')
  deprivation_oa.to_csv('lbth_census_2021_deprivation_oa.csv')

#merge deprivation data with spatial data
#deprivation_merge=merge_spatial_data(merged_wd_oa, deprivation_oa,"OA21CD", "GEOGRAPHY_CODE")

# %%
#read in relative deprivation 2021 dataset

try:
  deprivation_2021 = pd.read_csv('lbth_census_2021_deprivation_2021.csv')
except:
  deprivation_2021 = pd.read_csv('https://www.nomisweb.co.uk/api/v01/dataset/NM_2031_1.data.csv?date=latest&geography=645923010,2092957699,2013265927&c2021_dep_6=1...5&measures=20301')
  deprivation_2021.to_csv('lbth_census_2021_deprivation_2021.csv')

# %%
#read in relative deprivation 2021 dataset

try:
 deprivation_2011 = pd.read_csv('lbth_census_2021_deprivation_2011.csv')
except:
 deprivation_2011 = pd.read_csv('https://www.nomisweb.co.uk/api/v01/dataset/NM_519_1.data.csv?date=latest&geography=1946157257,2092957699,2013265927&rural_urban=0&c_deprived=1...5&measures=20100')
 deprivation_2011.to_csv('lbth_census_2021_deprivation_2011.csv')

# %%
#convert value to percent in 2011 dataset

deprivation_2011['OBS_VALUE'] = (
    np.select(
        condlist=[deprivation_2011['GEOGRAPHY_NAME'] == 'Tower Hamlets', deprivation_2011['GEOGRAPHY_NAME'] =='England', deprivation_2011['GEOGRAPHY_NAME'] =='London'],
        choicelist=[(deprivation_2011['OBS_VALUE']/101257)*100,(deprivation_2011['OBS_VALUE']/22063368)*100,(deprivation_2011['OBS_VALUE']/3266173)*100] 
        ))

# %%
#rename column deprivation column to allow for concatenate

deprivation_2011.rename(columns={'C_DEPRIVED_NAME': 'C2021_DEP_6_NAME'}, inplace=True)

# %%
#concatenate 2011 and 2021 dataframes 

deprivation_2011_2021=pd.concat([deprivation_2011,deprivation_2021])

# %%
# Replace multiple substrings

deprivation_2011_2021= deprivation_2011_2021.apply(lambda x: x.replace({'one':'1','two': '2',
    'three': '3','four': '4'},regex=True))

# %%
#split dataframe by deprivation index

any_dimension= deprivation_2011_2021[deprivation_2011_2021['C2021_DEP_6_NAME'].str.contains('any dimension',na=False)].reset_index(drop=True)

one_dimension=deprivation_2011_2021[deprivation_2011_2021['C2021_DEP_6_NAME'].str.contains('1',na=False)].reset_index(drop=True)

two_dimension=deprivation_2011_2021[deprivation_2011_2021['C2021_DEP_6_NAME'].str.contains('2',na=False)].reset_index(drop=True)

three_dimension=deprivation_2011_2021[deprivation_2011_2021['C2021_DEP_6_NAME'].str.contains('3',na=False)].reset_index(drop=True)

four_dimension=deprivation_2011_2021[deprivation_2011_2021['C2021_DEP_6_NAME'].str.contains('4',na=False)].reset_index(drop=True)


# %%
# create a new plot with a title and axis labels
p = figure(title="Household is not deprived in any dimension", x_axis_label='Year', y_axis_label='Percentage')

source = ColumnDataSource(any_dimension)

for (name, group), color in zip(any_dimension.groupby('GEOGRAPHY_NAME'), Viridis3):
    p.line(x=group.DATE, y=group.OBS_VALUE, legend_label=str(name), color=color,line_width=3)
    
p.xaxis.ticker=[2011,2021] #customise x axis tick values 

p.xaxis.axis_label_text_font_size = "20pt"
p.xaxis.major_label_text_font_size = "15pt"
p.xaxis.axis_label_text_font = "arial"
p.xaxis.axis_label_text_color = "black"

p.yaxis.axis_label_text_font_size = "20pt"
p.yaxis.major_label_text_font_size = "15pt"
p.yaxis.axis_label_text_font = "arial"
p.yaxis.axis_label_text_color = "black"

p.legend.location = "bottom_right"
p.legend.label_text_font_size = "15pt"
p.legend.label_text_font = "arial"
p.legend.label_text_color = "black"

p.title.text_font_size = '15pt'

show(p)

# %%
with st.sidebar:
    add_radio = st.radio(label='Variable selection', options=('Household deprivation','Homelessness'))

if add_radio == "Household deprivation":
     st.title('Household deprivation')
        deprivation_radio= st.radio("Deprivation index", ('Household is not deprived in any dimension',
     'Household is deprived in one dimension',
     'Household is deprived in two dimensions',
     'Household is deprived in three dimensions',
     'Household is deprived in four dimensions'))

    if deprivation_radio =='Household is not deprived in any dimension': 
        col1, col2=st.columns(2)
    with col1:
        plot_wards(deprivation_merge,column='C2021_DEP_6_NAME', string='Household is not deprived in any dimension',agg='mean',
         title='Percentage of Households')
    with col2:
        st.bokeh_chart(p, use_container_width=True)
    
    elif deprivation_radio =='Household is deprived in one dimension':  
    plot_wards(deprivation_merge,column='C2021_DEP_6_NAME', string='Household is deprived in one dimension',agg='mean',
       title='Percentage of Households')

    elif deprivation_radio =='Household is deprived in two dimensions': 
    plot_wards(deprivation_merge,column='C2021_DEP_6_NAME', string='Household is deprived in two dimensions',agg='mean',
       title='Percentage of Households')

     elif deprivation_radio =='Household is deprived in three dimensions': 
        plot_wards(deprivation_merge,column='C2021_DEP_6_NAME', string='Household is deprived in three dimensions',agg='mean',
       title='Percentage of Households')

    elif deprivation_radio== 'Household is deprived in four dimensions':
    plot_wards(deprivation_merge,column='C2021_DEP_6_NAME', string='Household is deprived in four dimensions',agg='mean',
       title='Percentage of Households')


