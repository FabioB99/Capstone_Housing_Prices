# -*- coding: utf-8 -*-
"""
Created on Tue May 10 15:39:15 2022

@author: Michael Meier, Silvan Liebherr, Fabio Bohren
"""

################################################
# Bibliotheken importieren & Daten Laden
################################################

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# Einstellungen zur Seite
st.set_page_config(
    page_title= "Housing Prices App",
    page_icon = "🏘️",
    layout="wide")

# Daten importieren
# @st.cache(allow_output_mutation=True)
def load_data():
    df = pd.read_csv("houses_data_dev.csv")
    return df

@st.cache(allow_output_mutation=True)
def load_model():
    filename = 'final_model.sav'
    loaded_model = pickle.load(open(filename, "rb"))
    return(loaded_model)

df = load_data()
model = load_model()


################################################
# Header
################################################

# Insert blank line at the top
st.markdown('#')
# Add a title + anchor and a title image
st.title("  \n  House Price Prediction ")

# Add an expandable page description with links to the corresponding section
with st.expander("See Page Description"):
     st.markdown("This Streamlit dashboard....")