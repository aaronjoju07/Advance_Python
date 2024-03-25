import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('/Users/aaronjoju/Documents/Advance_Python/practice/Iris.csv')
st.title("Iris Dataset")
# Sidebar
choice = st.sidebar.selectbox(
    'Which dataset would you like to display?',
    ('All data','Sepal','Petal'])
if choice =='All data':
   df=df
elif choice=='Sepal':
   df=df[['sepal length (cm)','sepal width (cm)','class']]
else:
   df=df[['petal length (cm)','petal width (cm)','class']]