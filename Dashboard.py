import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from PIL import Image
import pickle
import sklearn

st.set_page_config(page_title='NFL Football Stats and Predictor', layout='wide')
st.title('NFL Football Stats and Predictor')

st.markdown("""
This app provides NFL Football stats data!
*  We will also give a prediction on the playoff games for this year!
""")

#st.sidebar.header('Playoff Teams')
#selected_year = st.sidebar.selectbox('Year', list(reversed(range(2015,2021))))
st.sidebar.header('Playoff Teams')

teams_dict = {'Buffalo Bills' : {'Abbrev':'BUF', 'Logo' : 'Logos/Bills.png'}, 'Pittsburgh Steelers' : {'Abbrev':'PIT', 'Logo' : 'Logos/Steelers.png'}, 
              'Kansas City Chiefs' : {'Abbrev':'KAN', 'Logo' : 'Logos/Chiefs.png'}, 'Las Vegas Raiders' : {'Abbrev':'RAI', 'Logo' : 'Logos/Raiders.png'},
              'Tennessee Titans' : {'Abbrev':'OTI', 'Logo' : 'Logos/Titans.png'}, 'Los Angeles Rams' : {'Abbrev':'RAM', 'Logo' : 'Logos/Rams.png'},
              'New England Patriots' : {'Abbrev':'NWE', 'Logo' : 'Logos/Patriots.png'}, 'Tampa Bay Buccaneers' : {'Abbrev':'TAM', 'Logo' : 'Logos/Buccaneers.png'}, 
              'San Fransisco 49ers' : {'Abbrev':'SFO', 'Logo' : 'Logos/49ers.png'}, 'Cincinnati Bengals' : {'Abbrev':'CIN', 'Logo' : 'Logos/Bengals.png'}, 
              'Dallas Cowboys' : {'Abbrev':'DAL', 'Logo' : 'Logos/Cowboys.png'}, 'Philadelphia Eagles' : {'Abbrev':'PHI', 'Logo' : 'Logos/Eagles.png'}, 
              'Green Bay Packers' : {'Abbrev':'GNB', 'Logo' : 'Logos/Packers.png'}, 'Arizona Cardinals' : {'Abbrev':'CRD', 'Logo' : 'Logos/Cardinals.png'}}



# Sidebar - Team selection
#sorted_unique_team =["buf","pit","kan","rai","oti","ram","nwe","tam","sfo","cin","dal","phi","gnb","crd"]
sorted_unique_team = ["Buffalo Bills", "Pittsburgh Steelers", "Kansas City Chiefs","Las Vegas Raiders",
                      "Tennessee Titans","Los Angeles Rams","New England Patriots","Tampa Bay Buccaneers",
                      "San Fransisco 49ers","Cincinnati Bengals","Dallas Cowboys","Philadelphia Eagles",
                      "Green Bay Packers","Arizona Cardinals"]
selected_team = st.sidebar.selectbox("Teams", sorted_unique_team)

# Web scraping of NFL player stats
# "https://www.pro-football-reference.com/teams/ram/2021.htm"   # "https://www.pro-football-reference.com/teams/" + str(team) + "/2021.htm"
@st.cache
def load_data(team): #year,
    url = "https://www.pro-football-reference.com/teams/" + teams_dict[selected_team]['Abbrev'].lower() + "/2021.htm"
    df = pd.read_html(url, header = 1)
    df = df[1]
    return df
teamstats = load_data(selected_team) #selected_year, 

st.subheader('Display Selected Team Schedule & Game Results')
st.subheader('Current Team Selection: ' + selected_team)
st.image(teams_dict[selected_team]['Logo'], width = 500)
st.dataframe(teamstats)

# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href
st.markdown(filedownload(teamstats), unsafe_allow_html=True)

#bills = [st.image("chiefslogo.png", width=40)]
bills = Image.open("chiefslogo.png")
#rams =
#bengals =
#chiefs =
#cowboys =
#titans =
#packers =
#buccaneers =
#cardinals =
#patriots =
#eagles =
#fortyniners =
#steelers =
#raiders =

# image = Image.open('Packerslogo.png')
# st.image(image, caption='Sunrise by the mountains')

st.header("Superbowl Playoffs")
st.header("First round matchups")

col1, col2 = st.columns(2)
col1.subheader("Teams")
col1.markdown("AFC Game 1")
col1.image("Logos/Chiefs.png", width = 200)
col1.image("Logos/Steelers.png", width = 200)
col1.markdown("AFC Game 2")
col1.image("Logos/Bills.png", width = 200)
col1.image("Logos/Patriots.png", width = 200)
col1.markdown("AFC Game 3")
col1.image("Logos/Bengals.png", width = 200)
col1.image("Logos/Raiders.png", width = 200)
col1.markdown("NFC Game 1")
col1.image("Logos/Buccaneers.png", width = 200)
col1.image("Logos/Eagles.png", width = 200)
col1.markdown("NFC Game 2")
col1.image("Logos/Cowboys.png", width = 200)
col1.image("Logos/49ers.png", width = 200)
col1.markdown("NFC Game 3")
col1.image("Logos/Rams.png", width = 200)
col1.image("Logos/Cardinals.png", width = 200)
col1.markdown("AFC Bye team: ")
col1.image("Logos/Titans.png", width = 200)
col1.markdown("NFC Bye team: ")
col1.image("Logos/Packers.png", width = 200)
container = st.container()

#https://www.vhv.rs/dpng/d/409-4095070_download-new-england-patriots-png-hd-pat-the.png

button1 = st.button("Run Prediction")
if button1:
    st.write("prediction are being calculated...")
#    result = predict_model()

col2.subheader("Predictions")
col2.write("AFC Game 1 Winner:")
col2.subheader("this is the winner of game 1")
col2.write("AFC Game 2 Winner:")

col2.write("AFC Game 3 Winner:")

col2.write("NFC Game 1 Winner:")

col2.write("NFC Game 2 Winner:")

col2.write("NFC Game 3 Winner:")

col2.write("AFC Bye team: ")
col2.write("NFC Bye team: ")




st.header("Divisional round")
col1, col2 = st.columns(2)
col1.subheader("Teams")
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
col1.subheader("Teams")
col1.markdown("Super Bowl Game")

button4 = st.button("Run Prediction 4")
if button4:
    st.write("prediction are being calculated...")

col2.subheader("Predictions")
col2.write("Super Bowl Winner:")
