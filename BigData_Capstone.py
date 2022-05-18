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
     
st.markdown('#')

with st.expander("See Dataframe"):
     st.dataframe(data=df)
     

# Code für Sidebar
#Erstellung der Überschriften in der Sidebar
st.sidebar.title("Immobilienbewertung")
st.sidebar.markdown("Berechnen Sie jetzt den Wert Ihrer Liegenschaft")

st.sidebar.header("Details zu Ihrer Liegenschaft")

#Erstellung der Features in der Sidebar

quality = st.sidebar.slider("Generelle Qualität der Liegenschaft",
                           0, 10, 5)
#Einfügen einer Legende zu den Werten von quality
legende_qualität = '<p style="font-family:Courier; color:Red; font-size: 10px;">0 = sehr schlecht, 10 = exzellent</p>'
st.sidebar.markdown(legende_qualität, unsafe_allow_html=True)


df["GrLivArea"] = df["GrLivArea"].astype(int)
generellground = st.sidebar.number_input("Wohnfläche in sqf (ohne Kellerräume)",
                                  0, 8000, 2500, 1)
                        

df["1stFlrSF"] = df["1stFlrSF"].astype(int)
firstfloor = st.sidebar.number_input("Wohnfläche des ersten Stocks in sqf",
                                  0, 7000, 1000, 1)

df["2ndFlrSF"] = df["2ndFlrSF"].astype(int)
secondfloor = st.sidebar.number_input("Wohnfläche des zweiten Stocks in sqf",
                                  0, 3500, 1000, 1)

df["BsmtFinSF1"] = df["BsmtFinSF1"].astype(int)
kellerfläche = st.sidebar.number_input("Kellerfläche in sqf",
                                  0, 7000, 1000, 1)

df["LotArea"] = df["LotArea"].astype(int)
grundstücksfläche = st.sidebar.number_input("Grundstücksfläche in sqf",
                                  0, 250000, 150000, 1)

baujahr = st.sidebar.number_input("Baujahr",
                                  1850, 2022)

renovationsjahr = st.sidebar.number_input("Renovationsjahr",
                                  1850, 2022)
#Einfügen einer Legende für Renovationsjahr
legende_renovationsjahr = '<p style="font-family:Courier; color:Red; font-size: 10px;">Falls bisher keine Renovation stattfand, dann Renovationsjahr = Baujahr</p>'
st.sidebar.markdown(legende_renovationsjahr, unsafe_allow_html=True)

badezimmer = st.sidebar.number_input("Anzahl Badezimmer",
                                  0, 5)

garagenplätze = st.sidebar.number_input("Anzahl Garagenplätze",
                                       0, 10)

df["LotFrontage"] = df["LotFrontage"].astype(int)
einfahrt = st.sidebar.slider("Länge der Einfahrt in ft",
                               0, 500, 150, 1)

