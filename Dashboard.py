import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('NFL Football Stats and Predictor')

st.markdown("""
This app provides NFL Football stats data!
*  We will also give a prediction on the playoff games for this year!
""")

#st.sidebar.header('Playoff Teams')
#selected_year = st.sidebar.selectbox('Year', list(reversed(range(2015,2021))))
st.sidebar.header('Playoff Teams')

# Sidebar - Team selection
sorted_unique_team = ["cin","oti","buf","kan","gnb","tam","dal","ram"]
selected_team = st.sidebar.selectbox("Teams", sorted_unique_team)

# Web scraping of NFL player stats
# "https://www.pro-football-reference.com/teams/ram/2021.htm"   
# "https://www.pro-football-reference.com/teams/" + str(team) + "/2021.htm"
@st.cache
def load_data(team): #year,
    url = "https://www.pro-football-reference.com/teams/" + str(selected_team) + "/2021.htm"
    df = pd.read_html(url, header = 1)
    df = df[1]
    return df
teamstats = load_data(selected_team) #selected_year, 

st.subheader('Display Selected Team Schedule & Game Results')
st.dataframe(teamstats)

# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(teamstats), unsafe_allow_html=True)

#def convert_df(df):
    
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
#    return df.to_csv().encode('utf-8')

#csv = convert_df(teamstats)

#st.download_button(
#     label="Download data as CSV",
#     data=csv,
#     file_name='teamstats.csv',
#     mime='text/csv', )

