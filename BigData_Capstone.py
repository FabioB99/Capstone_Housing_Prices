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
st.title("Immobilienpreis Vorhersage")

# Add an expandable page description with links to the corresponding section
st.markdown("Das vorliegende Dashboard ermöglicht die Vorhersage von Immobilienpreisen. Dazu können in der Sidebar die entsprechenden Merkmale der persönlichen Liegenschaft ausgewählt werden. Auf Basis derer wird die Immobilie mit einem Verkaufspreis bewertet. Mithilfe der Datenvisualisierung können bestehende Datenpunkte analysiert und miteinander verglichen werden. Dies kann insbesondere bei der Einschätzung fremder, aber auch der eigenen Liegenschaft hilfreich sein.")
st.markdown('#')

################################################
# Sidebar
################################################

#Erstellung der Überschriften in der Sidebar
st.sidebar.title("Immobilienbewertung")
st.sidebar.markdown("Berechnen Sie jetzt den Wert Ihrer Liegenschaft")

st.sidebar.header("Details zu Ihrer Liegenschaft")


#Create features in the sidebar

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
einfahrt = st.sidebar.slider("Grundstücksgrenze in ft",
                               0, 500, 150, 1)


################################################
# Dateninspektion
################################################

st.subheader("Visualisierung der Daten")

col1, col2, col3  = st. columns([1,1,1])

# Create filter sliders
baujahr2 = col1.slider("Baujahr", int(df["YearBuilt"].min()), int(df["YearBuilt"].max()), (1900, 2000))
grundstücksfläche2 = col2.slider("Grundstücksfläche in sqf", int(df["LotArea"].min()), int(df["LotArea"].max()), (1300, 150000))
generellground2 = col3.slider("Wohnfläche in sqf", int(df["GrLivArea"].min()), int(df["GrLivArea"].max()), (1000, 5000))
quality2 = col1.slider('Zustand der Immobilie', int(df["OverallQual"].min()), int(df["OverallQual"].max()), (2, 8))  
badezimmer2 = col2.slider('Anzahl Badezimmer', int(df["FullBath"].min()), int(df["FullBath"].max()), (1, 2))  
garagenplätze2 = col3.slider('Anzahl Garagenplätze', int(df["GarageCars"].min()), int(df["GarageCars"].max()), (1, 3))

# creating filtered data set according to slider inputs
filtered_df = df.loc[(df["OverallQual"] >= quality2[0]) & (df["OverallQual"] <= quality2[1]) &
                     (df["LotArea"] >= grundstücksfläche2[0]) & (df["LotArea"] <= grundstücksfläche2[1]) &
                     (df["YearBuilt"] >= baujahr2[0]) & (df["YearBuilt"] <= baujahr2[1]) &
                     (df["FullBath"] >= badezimmer2[0]) & (df["FullBath"] <= badezimmer2[1]) &
                     (df["GarageCars"] >= garagenplätze2[0]) & (df["GarageCars"] <= garagenplätze2[1]) &
                     (df["GrLivArea"] >= generellground2[0]) & (df["GrLivArea"] <= generellground2[1]),:]
st.write("#")
with st.expander("Ganzes Datenset anzeigen"):
    st.dataframe(filtered_df)

st.write("#")

################################################
# Vorhersage
################################################

st.sidebar.write("#")

def create_pred_df():
    d = {'LotFrontage': int(einfahrt), 'LotArea': int(grundstücksfläche),
         'OverallQual': int(quality), 'YearBuilt': int(baujahr), 
         'YearRemodAdd': int(renovationsjahr), 'BsmtFinSF1': int(kellerfläche),
         '1stFlrSF': int(firstfloor),'2ndFlrSF': int(secondfloor),
         'FullBath': int(badezimmer), 'GarageCars': int(garagenplätze), 
         'GrLivArea': int(generellground)}     
    input_data = pd.DataFrame(data=d,index=[0])
    return input_data

# Start prediction
def make_prediction():
    prediction = model.predict(create_pred_df())
    price_output = str(int(prediction)) + " USD"
    st.sidebar.metric(label="Geschätzter Kaufpreis:", value=price_output)
    st.sidebar.success("Vorhersage erfolgreich👍")
    return price_output

if st.sidebar.button("Vorhersage durchführen"):
    make_prediction()
    

################################################
# Plots
################################################
       
# defining two columns for layouting plots 
row2_col1, row2_col2  = st. columns([1,1])

# Seaborn Chart Fig1
fig1 = plt.figure(figsize=(10,5))
p = sns.scatterplot(data=filtered_df, x="GrLivArea", y="SalePrice", hue="OverallQual")
p.set_xlabel("Wohnfläche in sqf", fontsize = 15)
p.set_ylabel("Verkaufspreis in USD", fontsize = 15)


# Put seaborn figure 1 in col 1 
row2_col1.subheader("Korrelation Wohnfläche & Verkaufspreis")
row2_col1.pyplot(fig1, use_container_width=True)

# Seaborn Chart Fig2
fig2 = plt.figure(figsize=(10,5))
q = sns.scatterplot(data=filtered_df, x="YearBuilt", y="SalePrice", hue="OverallQual")
q.set_xlabel("Baujahr", fontsize = 15)
q.set_ylabel("Verkaufspreis in USD", fontsize = 15)

# Put seaborn figure 2 in col 2 
row2_col2.subheader("Korrelation Baujahr & Verkaufspreis")
row2_col2.pyplot(fig2, use_container_width=True)

# defining three columns for layouting plots 
row3_col1, row3_col2  = st. columns([1,1])

# Seaborn Chart Fig3
fig3 = plt.figure(figsize=(10,5))
r = sns.histplot(filtered_df, x="SalePrice", hue="OverallQual")
r.set_xlabel("Verkaufspreis in USD", fontsize = 15)
r.set_ylabel("Anzahl Immobilien", fontsize = 15)

# Put seaborn figure 1 in col 1 
row3_col1.subheader("Verteilung nach Verkaufspreis")
row3_col1.pyplot(fig3, use_container_width=True)

fig4 = plt.figure(figsize=(10,5))
s = sns.histplot(filtered_df, x="OverallQual", hue=None, color="#98648c")
s.set_xlabel("Allgemeiner Immobilienzustand", fontsize = 15)
s.set_ylabel("Anzahl Immobilien", fontsize = 15)

# Put seaborn figure 1 in col 1 
row3_col2.subheader("Verteilung nach Immobilienzustand")
row3_col2.pyplot(fig4, use_container_width=True)
