import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(page_title='NFL Football Stats and Predictor', layout='wide')
st.title('NFL Football Stats and Predictor')

st.markdown("""
This app provides NFL Football stats data!
*  We will also give a prediction on the playoff games for this year!
""")

#st.sidebar.header('Playoff Teams')
#selected_year = st.sidebar.selectbox('Year', list(reversed(range(2015,2021))))
st.sidebar.header('Playoff Teams')

# Sidebar - Team selection
sorted_unique_team = ["cin","oti","buf","kan","gnb","tam","dal","ram","nwe","crd","phi"]
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
st.header("Superbowl Playoffs")
st.header("First round matchups")

col1, col2 = st.columns(2)
col1.subheader("teams")
col1.markdown("AFC Game 1")

col1.markdown("AFC Game 2")

col1.markdown("AFC Game 3")

col1.markdown("NFC Game 1")

col1.markdown("NFC Game 2")

col1.markdown("NFC Game 3")

col1.markdown("AFC Bye team: ")
col1.markdown("NFC Bye team: ")
container = st.container()
container.write("Kansa City Chiefs")
container.image("chiefslogo.png", width=40)


button1 = st.button("Run Prediction")
if button1:
    st.write("prediction are being calculated...")
#    result = predict_model()

col2.subheader("Predictions")
col2.write("AFC Game 1 Winner:")

col2.write("AFC Game 2 Winner:")

col2.write("AFC Game 3 Winner:")

col2.write("NFC Game 1 Winner:")

col2.write("NFC Game 2 Winner:")

col2.write("NFC Game 3 Winner:")

col2.write("AFC Bye team: ")
col2.write("NFC Bye team: ")




st.header("Divisional round")
col1, col2 = st.columns(2)
col1.subheader("teams")
col1.markdown("AFC Game 1")

col1.markdown("AFC Game 2")

col1.markdown("NFC Game 1")

col1.markdown("NFC Game 2")

button2 = st.button("Run Prediction 2")
if button2:
    st.write("prediction are being calculated...")

col2.subheader("Predictions")
col2.write("AFC Game 1 Winner:")

col2.write("AFC Game 2 Winner:")

col2.write("NFC Game 1 Winner:")

col2.write("NFC Game 2 Winner:")


st.header("Conference championships")
col1, col2 = st.columns(2)
col1.subheader("teams")
col1.markdown("AFC Final Game")

col1.markdown("NFC Final Game")

button3 = st.button("Run Prediction 3")
if button3:
    st.write("prediction are being calculated...")

col2.subheader("Predictions")
col2.write("AFC Final Winner:")

col2.write("NFC Final Winner:")


st.header("Super Bowl")
col1, col2 = st.columns(2)
col1.subheader("teams")
col1.markdown("Super Bowl Game")

button4 = st.button("Run Prediction 4")
if button4:
    st.write("prediction are being calculated...")

col2.subheader("Predictions")
col2.write("Super Bowl Winner:")
