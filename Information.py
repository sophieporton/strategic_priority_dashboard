# %%
import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px


# %%
# 2022 ward boundaries
try:
  wd22 = gpd.read_file('lbth_wd22.geojson')
except Exception:
  wd22 = gpd.read_file('https://gist.github.com/joel-lbth/081ff5112ac66e6365a9846a6bc79409/raw/5371719f7fb24c286ce5839fc69e45c0c6049518/lbth-wards.topojson')
  wd22.to_file('wd22.geojson', driver='GeoJSON')

# %%
# 2021 lsoa boundaries
try:
  lsoa21 = gpd.read_file('lbth_lsoa21.geojson')
except Exception:
  lsoa21 = gpd.read_file('https://gist.github.com/joel-lbth/5c1a6de137eb092bff61e82bd37996aa/raw/e8efb126c04045c6730d6bbbae3863dd5e80dd80/lbth-lsoa21.geojson')
  lsoa21.to_file('lbth_lsoa21.geojson', driver='GeoJSON')

# %%
# 2021 oa boundaries
try:
  oa21 = gpd.read_file('lbth_oa21.geojson')
except Exception:
  oa21 = gpd.read_file('https://gist.githubusercontent.com/joel-lbth/9cd8cbf8078d78954bb011a0927001a3/raw/cc247b708b2e52c549c03af5923b9dc8d3eec5af/lbth_oa21.geojson')
  oa21.to_file('lbth_oa21.geojson', driver='GeoJSON')

# %%
# ward oa lookup
try:
  wd_oa_lkup = pd.read_csv('wd_lsoa_lkup21.csv')
except Exception:
  wd_oa_lkup = pd.read_csv('https://gist.githubusercontent.com/joel-lbth/da1b6f54f1cd076bf7336be7336de04b/raw/2e25cc5c14ae4a7914dcfc0c0a64dc131bab84bd/lbth_oa21_ward_lookup.csv')
  wd_oa_lkup.to_csv('lbth_wd_oa_lkup.csv')

# %%
def merge_spatial_data(gdf, df, left_on="", right_on=""):
    gdf=gdf.merge(df, left_on=left_on, right_on=right_on)
    return gdf

# %%
#merge oa and ward df

merged_wd_oa=oa21.merge(wd_oa_lkup,left_on='OA21CD', right_on='oa21cd')

# %%
st.session_state['merged_wd_oa'] = merged_wd_oa

# %%
st.set_page_config(layout = "wide")
st.title("Ward profiles")
st.text('This is a web app to allow exploration of 2021 census data in Tower Hamlets by ward based on the 2022-2016 Tower Hamlets Strategic Plan')


