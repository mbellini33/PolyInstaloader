import streamlit as st
import pandas as pd
import numpy as np


data_frame = pd.read_csv("../uber.csv")
data_frame.rename(columns={'Lat':'lat','Lon':'lon'},inplace=True)
map_data = data_frame[["lat", "lon"]]

st.map(map_data)
