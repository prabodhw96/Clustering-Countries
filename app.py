import numpy as np
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import folium_static

@st.cache(persist=True, allow_output_mutation=True)
def load_data():
	data = pd.read_csv("clus.csv")
	return data

@st.cache(persist=True, allow_output_mutation=True)
def load_json():
	data = pd.read_json("world-countries.json")
	return data

clus = load_data()

gj = load_json()
gj = gj.assign(id=gj["features"].apply(pd.Series)["id"], name=gj["features"].apply(pd.Series)["properties"].apply(pd.Series)["name"])
gj = gj[gj.name.isin(list(clus.country.unique()))]

colors  = {}
colors[0] = "#a0522d"
colors[1] = "#0000ff"
colors[2] = "#2f4f4f"
colors[3] = "#98fb98"
colors[4] = "#ffff00"
colors[5] = "#ff69b4"
colors[6] = "#1e90ff"
colors[7] = "#ff00ff"
colors[8] = "#000000"
colors[9] = "#006400"
colors[10] = "#00ff00"
colors[11] = "#d8bfd8"
colors[12] = "#000080"
colors[13] = "#ffa500"
colors[14] = "#00ffff"
colors[15] = "#ff0000"

colours = clus.copy()
colours = colours.replace({"cluster":colors})
colours["colour1"] = colours["cluster"]
colours["colour2"] = colours["cluster"]
colours = colours.drop(columns=["cluster"])
colours = colours.set_index("country")

def style_fn(feature):
	cc = colours.loc[feature["properties"]["name"]]
	ss = {'fillColor':f'{cc[0]}', 'color':f'{cc[1]}'}
	return ss

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
st.markdown("### Select by")
option = st.radio("", ["Cluster", "Country"])
if option == "Cluster":
	c = st.radio(" ", ["Show all",0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
	if c == "Show all":
		m = folium.Map(location=[51.5074, 0.1728], zoom_start=1, control_scale=True, max_bounds=True)
		for r in gj.to_dict(orient="records"):
			folium.GeoJson(r["features"], name=r["name"], tooltip=r["name"], style_function=style_fn).add_to(m)
		folium_static(m)
	else:
		x = clus[clus["cluster"]==c]
		dx = gj[gj["name"].isin(x["country"].unique())].reset_index(drop=True)
		m = folium.Map(location = [51.5074, 0.1728], zoom_start=2, control_scale=True, max_bounds=True)
		for r in dx.to_dict(orient="records"):
			folium.GeoJson(r["features"], name=r["name"], tooltip=r["name"], style_function=style_fn).add_to(m)
		folium_static(m)
		st.write(list(x["country"].unique()))
else:
	country_list = list(clus["country"])
	country_list.sort()
	country = st.selectbox(" ", country_list)
	clus_id = int(clus[clus["country"]==country]["cluster"])
	x = clus[clus["cluster"]==clus_id]
	dx = gj[gj["name"].isin(x["country"].unique())].reset_index(drop=True)
	m = folium.Map(location = [51.5074, 0.1728], zoom_start=2, control_scale=True, max_bounds=True)
	for r in dx.to_dict(orient="records"):
		folium.GeoJson(r["features"], name=r["name"], tooltip=r["name"], style_function=style_fn).add_to(m)
	folium_static(m)
	st.write(list(x["country"].unique()))

st.write("Data: https://github.com/awslabs/open-data-docs/tree/main/docs/noaa/noaa-ghcn")