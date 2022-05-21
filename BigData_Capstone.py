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
@st.cache(allow_output_mutation=True)
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
st.title("House Price Prediction")

# Add an expandable page description with links to the corresponding section
with st.expander("See Page Description"):
     st.markdown("This Streamlit dashboard....")
     
st.markdown('#')



################################################
# Sidebar
################################################

#Erstellung der Überschriften in der Sidebar
st.sidebar.title("Immobilienbewertung")
st.sidebar.markdown("Berechnen Sie jetzt den Wert Ihrer Liegenschaft")

st.sidebar.header("Details zu Ihrer Liegenschaft")

#Erstellung der Features in der Sidebar

quality = st.sidebar.slider("Generelle Qualität der Liegenschaft",
                           0, 10, 5)
#Einfügen einer Legende zu den Werten von quality
legende_qualität = '<p style="font-family:Courier; color:grey; font-size: 10px;">0 = sehr schlecht, 10 = exzellent</p>'
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
legende_renovationsjahr = '<p style="font-family:Courier; color:grey; font-size: 10px;">Falls bisher keine Renovation stattfand, dann Renovationsjahr = Baujahr</p>'
st.sidebar.markdown(legende_renovationsjahr, unsafe_allow_html=True)

badezimmer = st.sidebar.number_input("Anzahl Badezimmer",
                                  0, 5)

garagenplätze = st.sidebar.number_input("Anzahl Garagenplätze",
                                       0, 10)

df["LotFrontage"] = df["LotFrontage"].astype(int)
einfahrt = st.sidebar.slider("Länge der Einfahrt in ft",
                               0, 500, 150, 1)



################################################
# Vorhersage
################################################

st.subheader("Kaufpreis vorhersagen:")
st.markdown("Erstellt eine Vorhersage für den Marktpreis basierend auf den eingegebenen Werten")

def create_pred_df():
    d = {'LotFrontage': int(einfahrt), 'LotArea': int(grundstücksfläche),
         'OverallQual': int(quality), 'YearBuilt': int(baujahr), 
         'YearRemodAdd': int(renovationsjahr), 'BsmtFinSF1': int(kellerfläche),
         '1stFlrSF': int(firstfloor),'2ndFlrSF': int(secondfloor),
         'FullBath': int(badezimmer), 'GarageCars': int(garagenplätze), 
         'GrLivArea': int(generellground)}     
    input_data = pd.DataFrame(data=d,index=[0])
    return input_data

# Vorhersage durchführen
def make_prediction():
    prediction = model.predict(create_pred_df())
    price_output = str(int(prediction)) + " USD"
    st.write("#")    
    st.metric(label="Estimated Price:", value=price_output)

row1_col1, row1_col2, row1_col3 = st.columns([1,1,1])

if row1_col1.button("Start Prediction"):
    st.write(make_prediction())



st.write("#")





################################################
# Grafiken
################################################
       
st.subheader("Visualisierung der Daten:")

with st.expander("Ganzes Datenset anzeigen"):
     st.dataframe(data=df)

st.write("#")


# defining two columns for layouting plots 
row2_col1, row2_col2  = st. columns([1,1])

# Seaborn Chart Fig1
fig1 = plt.figure(figsize=(10,5))
sns.scatterplot(data=df, x="LotArea", y="SalePrice", hue="OverallQual")
plt.title("Sale Price & Lot Area")

# Put seaborn figure 1 in col 1 
row2_col1.subheader("Sale Price & Lot Area")
row2_col1.pyplot(fig1, use_container_width=True)


# Seaborn Chart Fig2
fig2 = plt.figure(figsize=(10,5))
sns.scatterplot(data=df, x="SalePrice", y="YearBuilt", hue="OverallQual")
plt.title("Sale Price & Year Built")

# Put seaborn figure 2 in col 2 
row2_col2.subheader("SalePrice & Year Built")
row2_col2.pyplot(fig2, use_container_width=True)

# defining three columns for layouting plots 
row3_col1, row3_col2  = st. columns([1,1])

# Seaborn Chart Fig3
fig3 = plt.figure(figsize=(10,5))
sns.scatterplot(data=df, x="LotFrontage", y="SalePrice", hue="OverallQual")
plt.title("Lot Frontage & Sale Price")

# Put seaborn figure 1 in col 1 
row3_col1.subheader("Lot Frontage & Sale Price")
row3_col1.pyplot(fig3, use_container_width=True)

# Seaborn Chart Fig4
fig4 = plt.figure(figsize=(10,5))
sns.scatterplot(data=df, x="YearRemodAdd", y="GrLivArea", hue="SalePrice")
plt.title("Renovation Year & General Living Area")

# Put seaborn figure 4 in col 2
row3_col2.subheader("Renovation Year & General Living Area")
row3_col2.pyplot(fig4, use_container_width=True)
