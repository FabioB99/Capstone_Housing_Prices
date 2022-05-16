# -*- coding: utf-8 -*-
"""
Created on Tue May 10 15:39:15 2022

@author: Michael Meier, Silvan Liebherr, Fabio Bohren
"""

################################################
# Setup
################################################

#Pfad jeweils an die eigene Ablage anpassen
path = "G:/Meine Ablage/Colab Notebooks/Capstone/Programm/" #Pfadi Fabio

# Um das Programm zu starten:
# 1. Anaconda Prompt starten, 2. Programm ausführen, 3. Konsolen-Ouput in Prompot kopieren und ausführen
print('streamlit run ' + '"' + path + 'BigData_Capstone.py"')

################################################
# Bibliotheken importieren & Daten Laden
################################################

import streamlit as st
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
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
    df = pd.read_csv(path + "houses_data_dev.csv")
    return df

@st.cache(allow_output_mutation=True)
def load_model():
    filename = path + 'final_model.sav'
    loaded_model = pickle.load(open(filename, "rb"))
    return(loaded_model)

df = load_data()
model = load_model()


