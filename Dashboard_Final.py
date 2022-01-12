import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from PIL import Image
import pickle
import sklearn
import os

from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

st.set_page_config(page_title='NFL Football Stats and Predictor', layout='wide')
st.image('./Logos/SBanner.jpeg')
st.title('NFL Football Stats and Predictor')

model = pickle.load(open('MLP_model.sav','rb'))
path = ("./resources/Team_df.csv")
com_data = pd.read_csv(path)

# get index of every team's data
team_index = com_data['Team']

# Remove Opponent, Score, Result
mlp_model_data = com_data[['Team', 'Opp', 'TmScore', 'O_1stD', 'O_Tot_yd', 'O_P_Yd', 'O_R_Yd', 'O_TO',
                         'D_1stD', 'D_Tot_Yd', 'D_P_Yd', 'D_R_Yd', 'D_TO', 'Home','Prediction_LR','Prediction_ADA']]
# change to season stats
season_stats = ['O_1stD', 'O_Tot_yd', 'O_P_Yd', 'O_R_Yd', 'O_TO',
                         'D_1stD', 'D_Tot_Yd', 'D_P_Yd', 'D_R_Yd', 'D_TO']

mlp_model_data[season_stats] = mlp_model_data[season_stats] * 16

# standardise the data
from sklearn import preprocessing

sd_data = ['O_1stD', 'O_Tot_yd', 'O_P_Yd', 'O_R_Yd', 'O_TO',
                         'D_1stD', 'D_Tot_Yd', 'D_P_Yd', 'D_R_Yd', 'D_TO','Prediction_LR','Prediction_ADA']

mlp_model_data[sd_data] = preprocessing.scale(mlp_model_data[sd_data])

#get indexs of every teams
team_index = com_data['Team']

mlp_model_data = pd.get_dummies(mlp_model_data)

pd.options.display.max_rows = None

pd.options.display.max_columns = None

# Create playoff test dataset from season averages

def Score_Predictor(home_team, away_team):
    team1 = home_team
    team2 = away_team
    
    team1_data = mlp_model_data[com_data['Team'] == team1].drop('TmScore', axis=1).reset_index(drop=True)
    team2_data = mlp_model_data[com_data['Team'] == team2].drop('TmScore', axis=1).reset_index(drop=True)
    
    week_slice = slice(0,16)
    
    #1 Remove if no team names
    team1_test = pd.DataFrame(team1_data[week_slice].mean(axis=0)).T #select week to use as average
    #team1_test  #This was the line printing that extra dataframe onto the Dashboard
    opp_columns = team1_test.filter(like='Opp').columns
    
    team1_test[opp_columns] = 0
    team1_test['Opp_' + team2] = 1
    team1_test['Home'] = 1
    
    #2
    team2_test = pd.DataFrame(team2_data[week_slice].mean(axis=0)).T #select week to use as average
    opp_columns = team2_test.filter(like='Opp').columns
    
    team2_test[opp_columns] = 0
    team2_test['Opp_' + team1] = 1
    team2_test['Home'] = 1 # change to remove home field advantage
    
    # head to head matchup
    team1_test[['D_1stD','D_Tot_Yd','D_P_Yd','D_R_Yd','D_TO']] = team2_test[['O_1stD','O_Tot_yd','O_P_Yd','O_R_Yd','O_TO']]
    team2_test[['D_1stD','D_Tot_Yd','D_P_Yd','D_R_Yd','D_TO']] = team1_test[['O_1stD','O_Tot_yd','O_P_Yd','O_R_Yd','O_TO']]
    
    X_Playoff_test = pd.concat([team1_test, team2_test])
    X_Playoff_test.fillna(0, inplace = True) # added to address the NANs that was causing the error
    
    scores = model.predict(X_Playoff_test)
    print(team1, "will score", round(scores[0], 1))
    print(team2, "will score", round(scores[1], 1))
    
    if scores[0] > scores[1]:
        winner = team1
    else:
        winner = team2
        
    print(winner, "are the WINNERS!!!")
    
    return scores, winner


scores, winner = Score_Predictor('Philadelphia Eagles', 'Tampa Bay Buccaneers')



st.markdown("""
This app provides NFL Football stats data!
*  We will also give a prediction on the playoff games for this year!
""")

#st.sidebar.header('Playoff Teams')
#selected_year = st.sidebar.selectbox('Year', list(reversed(range(2015,2021))))
st.sidebar.header('Playoff Teams')


teams_dict = {'Buffalo Bills' : {'Abbrev':'BUF', 'Logo' : 'Logos/Bills.png', 'Seed' : 3}, 'Pittsburgh Steelers' : {'Abbrev':'PIT', 'Logo' : 'Logos/Steelers.png', 'Seed' : 7}, 
              'Kansas City Chiefs' : {'Abbrev':'KAN', 'Logo' : 'Logos/Chiefs.png', 'Seed' : 2}, 'Las Vegas Raiders' : {'Abbrev':'RAI', 'Logo' : 'Logos/Raiders.png', 'Seed' : 5},
              'Tennessee Titans' : {'Abbrev':'OTI', 'Logo' : 'Logos/Titans.png', 'Seed' : 1}, 'Los Angeles Rams' : {'Abbrev':'RAM', 'Logo' : 'Logos/Rams.png', 'Seed' : 4},
              'New England Patriots' : {'Abbrev':'NWE', 'Logo' : 'Logos/Patriots.png', 'Seed' : 6}, 'Tampa Bay Buccaneers' : {'Abbrev':'TAM', 'Logo' : 'Logos/Buccaneers.png', 'Seed' : 2}, 
              'San Francisco 49ers' : {'Abbrev':'SFO', 'Logo' : 'Logos/49ers.png', 'Seed' : 6}, 'Cincinnati Bengals' : {'Abbrev':'CIN', 'Logo' : 'Logos/Bengals.png', 'Seed' : 4}, 
              'Dallas Cowboys' : {'Abbrev':'DAL', 'Logo' : 'Logos/Cowboys.png', 'Seed' : 3}, 'Philadelphia Eagles' : {'Abbrev':'PHI', 'Logo' : 'Logos/Eagles.png', 'Seed' : 7}, 
              'Green Bay Packers' : {'Abbrev':'GNB', 'Logo' : 'Logos/Packers.png', 'Seed' : 1}, 'Arizona Cardinals' : {'Abbrev':'CRD', 'Logo' : 'Logos/Cardinals.png', 'Seed' : 5}}



# Sidebar - Team selection
#sorted_unique_team =["buf","pit","kan","rai","oti","ram","nwe","tam","sfo","cin","dal","phi","gnb","crd"]
sorted_unique_team = ["Buffalo Bills", "Pittsburgh Steelers", "Kansas City Chiefs","Las Vegas Raiders",
                      "Tennessee Titans","Los Angeles Rams","New England Patriots","Tampa Bay Buccaneers",
                      "San Francisco 49ers","Cincinnati Bengals","Dallas Cowboys","Philadelphia Eagles",
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
Buffalo_Bills = Image.open("Logos/Bills.png")
Pittsburgh_Steelers = Image.open("Logos/Steelers.png")
Kansas_City_Chiefs = Image.open("Logos/Chiefs.png")
Las_Vegas_Raiders = Image.open("Logos/Raiders.png")
Tennessee_Titans = Image.open("Logos/Titans.png")
Los_Angeles_Rams = Image.open("Logos/Rams.png")
New_England_Patriots = Image.open("Logos/Patriots.png")
Tampa_Bay_Buccaneers = Image.open("Logos/Buccaneers.png")
San_Francisco_49ers = Image.open("Logos/49ers.png")
Cincinnati_Bengals = Image.open("Logos/Bengals.png")
Dallas_Cowboys = Image.open("Logos/Cowboys.png")
Philadelphia_Eagles = Image.open("Logos/Eagles.png")
Green_Bay_Packers = Image.open("Logos/Packers.png")
Arizona_Cardinals = Image.open("Logos/Cardinals.png")


# image = Image.open('Packerslogo.png')
# st.image(image, caption='Sunrise by the mountains')

st.header("Superbowl Playoffs")
st.header("First round matchups")

col1, col2 = st.columns(2)
col1.subheader("Teams")
col1.markdown("AFC Game 1")
col1.image(teams_dict['Kansas City Chiefs']['Logo'], width = 200)
col1.image(teams_dict['Pittsburgh Steelers']['Logo'], width = 200)
col1.markdown("AFC Game 2")
col1.image(teams_dict['Buffalo Bills']['Logo'], width = 200)
col1.image(teams_dict['New England Patriots']['Logo'], width = 200)
col1.markdown("AFC Game 3")
col1.image(teams_dict['Cincinnati Bengals']['Logo'], width = 200)
col1.image(teams_dict['Las Vegas Raiders']['Logo'], width = 200)
col1.markdown("NFC Game 1")
col1.image(teams_dict['Tampa Bay Buccaneers']['Logo'], width = 200)
col1.image(teams_dict['Philadelphia Eagles']['Logo'], width = 200)
col1.markdown("NFC Game 2")
col1.image(teams_dict['Dallas Cowboys']['Logo'], width = 200)
col1.image(teams_dict['San Francisco 49ers']['Logo'], width = 200)
col1.markdown("NFC Game 3")
col1.image(teams_dict['Los Angeles Rams']['Logo'], width = 200)
col1.image(teams_dict['Arizona Cardinals']['Logo'], width = 200)
col1.markdown("AFC Bye team: ")
col1.image(teams_dict['Tennessee Titans']['Logo'], width = 200)
col1.markdown("NFC Bye team: ")
col1.image(teams_dict['Green Bay Packers']['Logo'], width = 200)
container = st.container()

#https://www.vhv.rs/dpng/d/409-4095070_download-new-england-patriots-png-hd-pat-the.png
winner = ""
button1 = st.button("Run Prediction")
if button1:
    st.write("prediction are being calculated...")    
    scores1, afc_winner1 = Score_Predictor('Kansas City Chiefs', 'Pittsburgh Steelers')
    scores2, afc_winner2 = Score_Predictor('Buffalo Bills', 'New England Patriots')
    scores3, afc_winner3 = Score_Predictor('Cincinnati Bengals', 'Las Vegas Raiders')
    scores4, nfc_winner1 = Score_Predictor('Tampa Bay Buccaneers', 'Philadelphia Eagles')
    scores5, nfc_winner2 = Score_Predictor('Dallas Cowboys', 'San Francisco 49ers')
    scores6, nfc_winner3 = Score_Predictor('Los Angeles Rams', 'Arizona Cardinals')
    
    col2.subheader("Predictions")
    col2.write("AFC Game 1 Winner:")
    #col2.subheader(f"this is the winner of game 1:{scores1}")
    col2.image(teams_dict[afc_winner1]['Logo'])

    col2.write("AFC Game 2 Winner:")
    col2.image(teams_dict[afc_winner2]['Logo'])
    #col2.subheader(f"this is the winner of game 2:{winner2}")

    col2.write("AFC Game 3 Winner:")
    col2.image(teams_dict[afc_winner3]['Logo'])
    #col2.subheader(f"this is the winner of game 3:{winner3}")

    col2.write("NFC Game 1 Winner:")
    col2.image(teams_dict[nfc_winner1]['Logo'])
    #col2.subheader(f"this is the winner of game 1:{winner4}")

    col2.write("NFC Game 2 Winner:")
    col2.image(teams_dict[nfc_winner2]['Logo'])
    #col2.subheader(f"this is the winner of game 2:{winner5}")

    col2.write("NFC Game 3 Winner:")
    col2.image(teams_dict[nfc_winner3]['Logo'])
    #col2.subheader(f"this is the winner of game 3:{winner6}")

    col2.write("AFC Bye team: ")
    col2.image(teams_dict['Tennessee Titans']['Logo'])

    col2.write("NFC Bye team: ")
    col2.image(teams_dict['Green Bay Packers']['Logo'])
    
    # Original Code for round 2 added to the first prediction button
    
    afc_lowest = ''
    afc_team1 = ''
    afc_team2 = ''

    if (teams_dict[afc_winner1]['Seed'] > teams_dict[afc_winner2]['Seed']) and (teams_dict[afc_winner1]['Seed'] > teams_dict[afc_winner3]['Seed']):
        afc_lowest = afc_winner1
        afc_team1 = afc_winner2
        afc_team2 = afc_winner3
    elif (teams_dict[afc_winner2]['Seed'] > teams_dict[afc_winner1]['Seed']) and (teams_dict[afc_winner2]['Seed'] > teams_dict[afc_winner3]['Seed']):
        afc_lowest = afc_winner2
        afc_team1 = afc_winner1
        afc_team2 = afc_winner3
    elif (teams_dict[afc_winner3]['Seed'] > teams_dict[afc_winner1]['Seed']) and (teams_dict[afc_winner3]['Seed'] > teams_dict[afc_winner2]['Seed']):
        afc_lowest = afc_winner3
        afc_team1 = afc_winner1
        afc_team2 = afc_winner2
    
    
    nfc_lowest = ''
    nfc_team1 = ''
    nfc_team2 = ''

    if (teams_dict[nfc_winner1]['Seed'] > teams_dict[nfc_winner2]['Seed']) and (teams_dict[nfc_winner1]['Seed'] > teams_dict[nfc_winner3]['Seed']):
        nfc_lowest = nfc_winner1
        nfc_team1 = nfc_winner2
        nfc_team2 = nfc_winner3
    elif (teams_dict[nfc_winner2]['Seed'] > teams_dict[nfc_winner1]['Seed']) and (teams_dict[nfc_winner2]['Seed'] > teams_dict[nfc_winner3]['Seed']):
        nfc_lowest = nfc_winner2
        nfc_team1 = nfc_winner1
        nfc_team2 = nfc_winner3
    elif (teams_dict[nfc_winner3]['Seed'] > teams_dict[nfc_winner1]['Seed']) and (teams_dict[nfc_winner3]['Seed'] > teams_dict[nfc_winner2]['Seed']):
        nfc_lowest = nfc_winner3
        nfc_team1 = nfc_winner1
        nfc_team2 = nfc_winner2

    
    st.header("Divisional round")
    col1, col2 = st.columns(2)
    col1.subheader("Teams")
    col1.markdown("AFC Game 1")
    col1.image(teams_dict['Tennessee Titans']['Logo'], width = 200)
    col1.image(teams_dict[afc_lowest]['Logo'], width = 200)

    col1.markdown("AFC Game 2")
    col1.image(teams_dict[afc_team1]['Logo'], width = 200)
    col1.image(teams_dict[afc_team2]['Logo'], width = 200)

    col1.markdown("NFC Game 1")
    col1.image(teams_dict['Green Bay Packers']['Logo'], width = 200)
    col1.image(teams_dict[nfc_lowest]['Logo'], width = 200)

    col1.markdown("NFC Game 2")
    col1.image(teams_dict[nfc_team1]['Logo'], width = 200)
    col1.image(teams_dict[nfc_team2]['Logo'], width = 200)

    #button2 = st.button("Run Prediction 2")
    #if button2:
    st.write("prediction coming up...")
    scores7, winner7 = Score_Predictor('Tennessee Titans', afc_lowest)
    scores8, winner8 = Score_Predictor(afc_team1, afc_team2)
    scores9, winner9 = Score_Predictor('Green Bay Packers', nfc_lowest)
    scores10, winner10 = Score_Predictor(nfc_team1, nfc_team2)
   

    col2.subheader("Predictions")
    col2.write("AFC Game 1 Winner:")
    col2.image(teams_dict[winner7]['Logo'])

    col2.write("AFC Game 2 Winner:")
    col2.image(teams_dict[winner8]['Logo'])

    col2.write("NFC Game 1 Winner:")
    col2.image(teams_dict[winner9]['Logo'])

    col2.write("NFC Game 2 Winner:")
    col2.image(teams_dict[winner10]['Logo'])
        

    st.header("Conference championships")
    col1, col2 = st.columns(2)
    col1.subheader("teams")
    col1.markdown("AFC Final Game")
    col1.image(teams_dict[winner7]['Logo'], width = 200)
    col1.image(teams_dict[winner8]['Logo'], width = 200)

    col1.markdown("NFC Final Game")
    col1.image(teams_dict[winner9]['Logo'], width = 200)
    col1.image(teams_dict[winner10]['Logo'], width = 200)

        #button3 = st.button("Run Prediction 3")
        #if button3:
    st.write("prediction are being calculated...")
    scores11, winner11 = Score_Predictor(winner7, winner8)
    scores12, winner12 = Score_Predictor(winner9, winner10)

    col2.subheader("Predictions")
    col2.write("AFC Final Winner:")
    col2.image(teams_dict[winner11]['Logo'])
            
    col2.write("NFC Final Winner:")
    col2.image(teams_dict[winner12]['Logo'])
            
    

    st.header("Super Bowl")
    col1, col2 = st.columns(2)
    col1.image(teams_dict[winner11]['Logo'], width = 200)
    col1.image(teams_dict[winner12]['Logo'], width = 200)

          #  button4 = st.button("Run Prediction 4")
            #if button4:
    st.write("prediction are being calculated...")
    col2.write("Super Bowl Winner:")
    scores11, winner13 = Score_Predictor(winner11, winner12)
                
                
    col2.image(teams_dict[winner13]['Logo'])