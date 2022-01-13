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

st.set_page_config(page_title='Preadico: Super Bowl LVI', layout='wide')
st.image('./Logos/SBanner.jpeg')
st.title('Praedico: Road to Super Bowl LVI')

models = {'Logistic Regression': {'load' : pickle.load(open('LR_model.sav','rb'))},
         'Gradien Boosting': {'load' : pickle.load(open('GB_model.sav','rb'))},
         'MLP Regression': {'load' : pickle.load(open('MLP_model.sav','rb'))},
         'Random Forest': {'load' : pickle.load(open('RF_model.sav','rb'))}
         }
sorted_models = ['Logistic Regression', 'Gradien Boosting', 'MLP Regression', 'Random Forest']

path = ("./resources/Team_df.csv")
com_data = pd.read_csv(path)

st.markdown("""
Praedico is an online application that allows our users to fair a better chance of predicting the winner of the Super Bowl. Without a doubt the value of the NFL betting market is challenging to accurately estimate. The value of the sports betting market is anywhere between 700 Billion to 1 Trillion with an illegal market estimated at 500 Billion. If your goal is to make money, we can help you achieve that goal with a higher probabilty.


Thank you for using our application. We look forward to winning with you. May the Praedico be with you!

** Disclaimer: For informational purposes only. This is not betting advice. 
""")

#st.sidebar.header('Playoff Teams')
#selected_year = st.sidebar.selectbox('Year', list(reversed(range(2015,2021))))
st.sidebar.header('Playoff Teams')


teams_dict = {'Buffalo Bills' : {'Abbrev':'BUF', 'Logo' : 'Logos/Bills.png', 'Seed' : 3, 'Blurb' : "Buffalo Bills (11-6), champions, AFC East. The Bills won the division and kept this seed with a home win over the Jets. They finish a game behind the co-AFC leaders and a game ahead of the Bengals after being the AFC's No. 2 in last year's playoffs."},
              'Pittsburgh Steelers' : {'Abbrev':'PIT', 'Logo' : 'Logos/Steelers.png', 'Seed' : 7, 'Blurb' : "Pittsburgh Steelers (9-7-1), second place, AFC North. The Steelers got into the playoffs to extend the career of Ben Roethlisberger by beating the Ravens in Week 18 while the Jaguars beat the Colts and the Raiders beat the Chargers."}, 
              'Kansas City Chiefs' : {'Abbrev':'KAN', 'Logo' : 'Logos/Chiefs.png', 'Seed' : 2, 'Blurb' : "Kansas City Chiefs (12-5), champions, AFC West. The Chiefs will settle for the No. 2 seed after beating the Broncos in Week 18 because they lost head-to-head to the Titans in Week 7. They did win Super Bowl 54 coming from this position behind the Ravens."}, 
              'Las Vegas Raiders' : {'Abbrev':'RAI', 'Logo' : 'Logos/Raiders.png', 'Seed' : 5, 'Blurb' : "Las Vegas Raiders (10-7), second place, AFC West. The Raiders moved into playoff position with the Colts, whom they beat in Week 17, being upset by the Jaguars in Week 18. They earned a playoff berth with the wild overtime win over the Chargers on Sunday night."},
              'Tennessee Titans' : {'Abbrev':'OTI', 'Logo' : 'Logos/Titans.png', 'Seed' : 1, 'Blurb' : "Tennessee Titans (12-5), champions, AFC South. The Titans held on against the Texans in Week 18 to stay ahead of the Chiefs and clinch the No. 1 seed. They have home-field advantage in the AFC playoffs and the lone bye. The conference road to Super Bowl 56 will go through Nashviille."}, 
              'Los Angeles Rams' : {'Abbrev':'RAM', 'Logo' : 'Logos/Rams.png', 'Seed' : 4, 'Blurb' : "Los Angeles Rams (12-5), champions, NFC West. The Rams failed to beat the 49ers in Week 18 but still took back the division crown with the Cardinals losing another West matchup to the Seahawks at home. They cost themselves a No. 2 seed and now need to play a third game against the Cardinals."},
              'New England Patriots' : {'Abbrev':'NWE', 'Logo' : 'Logos/Patriots.png', 'Seed' : 6, 'Blurb' : "New England Patriots (10-7), second place, AFC East. The Patriots lost to the Dolphins in Week 18, but they had already lost the East title when the Bills beat the Jets. They dropped to No. 6 with the Raiders beating the Chargers on Sunday night because of losing the tiebreaker."},
              'Tampa Bay Buccaneers' : {'Abbrev':'TAM', 'Logo' : 'Logos/Buccaneers.png', 'Seed' : 2, 'Blurb' : "Tampa Bay Buccaneers (13-4), champions, NFC South. The Buccaneers beat the Panthers and moved up to No. 2 because the Rams, to whom they lost in Week 3, lost to the 49ers. They finished behind the Packers because of a lesser confference record and ahead of the Cowboys, up a full game and a head-to-head tiebreaker from Week 1."}, 
              'San Francisco 49ers' : {'Abbrev':'SFO', 'Logo' : 'Logos/49ers.png', 'Seed' : 6, 'Blurb' : "San Francisco 49ers (10-7), third place, NFC West. The 49ers locked down the second wild card by beating the Rams in overtime in Week 18. They held off the winning Saints and got up a full game on the losing Eagles, whom they also beat in Week 2."}, 
              'Cincinnati Bengals' : {'Abbrev':'CIN', 'Logo' : 'Logos/Bengals.png', 'Seed' : 4, 'Blurb' : "Cincinnati Bengals (10-7), champions, AFC North. The Bengals rested key players because of injuries and other reasons and lost without Joe Burrow and Joe Mixon at the Browns in Week 18. They were set to stay here behind the East champions."}, 
              'Dallas Cowboys' : {'Abbrev':'DAL', 'Logo' : 'Logos/Cowboys.png', 'Seed' : 3, 'Blurb' : "Dallas Cowboys (12-5), champions, NFC East. The Cowboys rebounded to rout the resting Eagles in Week 18 after they lost to the Cardinals in a failed comeback in Week 17. They were able to jump the losing Rams because of winning the conference-record tiebreaker over them."}, 
              'Philadelphia Eagles' : {'Abbrev':'PHI', 'Logo' : 'Logos/Eagles.png', 'Seed' : 7, 'Blurb' : "Philadelphia Eagles (9-8), second place, NFC East. The Eagles rested players against the Cowboys in Week 18 after they had already clinched a wild-card spot in Week 17. They stayed ahead of the winning Saints because of beating that team in Week 11."}, 
              'Green Bay Packers' : {'Abbrev':'GNB', 'Logo' : 'Logos/Packers.png', 'Seed' : 1,  'Blurb' : "Green Bay Packers (13-4), champions, NFC North. The Packers clinched the No. 1 seed, the lone bye and the Lambeau home-field advantage in the NFC playoffs with their win over the Vikings in Week 17, matching their win total of the previous two seasons with Aaron Rodgers under Matt LaFleur with one more game left in the new schedule. They lost in Week 18 while resting Rodgers and other regulars in the second half against the Lions."}, 
              'Arizona Cardinals' : {'Abbrev':'CRD', 'Logo' : 'Logos/Cardinals.png', 'Seed' : 5, 'Blurb' : "Arizona Cardinals (11-6), second place, NFC West. The Cardinals could have won the division with the Rams losing but they also lost to the Seahawks. They will settle for the top wild-card spot and a rematch with the Rams in the wild-card playoffs."}}


# Sidebar - Team selection
#sorted_unique_team =["buf","pit","kan","rai","oti","ram","nwe","tam","sfo","cin","dal","phi","gnb","crd"]
sorted_unique_team = ["Buffalo Bills", "Pittsburgh Steelers", "Kansas City Chiefs","Las Vegas Raiders",
                      "Tennessee Titans","Los Angeles Rams","New England Patriots","Tampa Bay Buccaneers",
                      "San Francisco 49ers","Cincinnati Bengals","Dallas Cowboys","Philadelphia Eagles",
                      "Green Bay Packers","Arizona Cardinals"]

selected_team = st.sidebar.selectbox("Teams", sorted_unique_team)

selected_model = st.sidebar.selectbox("Choose your Model", sorted_models)

# get index of every team's data
team_index = com_data['Team']

# Remove Opponent, Score, Result
model_data = com_data[['Team', 'Opp', 'TmScore', 'O_1stD', 'O_Tot_yd', 'O_P_Yd', 'O_R_Yd', 'O_TO',
                         'D_1stD', 'D_Tot_Yd', 'D_P_Yd', 'D_R_Yd', 'D_TO', 'Home','Prediction_LR','Prediction_ADA']]
# change to season stats
season_stats = ['O_1stD', 'O_Tot_yd', 'O_P_Yd', 'O_R_Yd', 'O_TO',
                         'D_1stD', 'D_Tot_Yd', 'D_P_Yd', 'D_R_Yd', 'D_TO']

model_data[season_stats] = model_data[season_stats] * 16

# standardise the data
from sklearn import preprocessing

sd_data = ['O_1stD', 'O_Tot_yd', 'O_P_Yd', 'O_R_Yd', 'O_TO',
                         'D_1stD', 'D_Tot_Yd', 'D_P_Yd', 'D_R_Yd', 'D_TO','Prediction_LR','Prediction_ADA']

model_data[sd_data] = preprocessing.scale(model_data[sd_data])

#get indexs of every teams
team_index = com_data['Team']

model_data = pd.get_dummies(model_data)

pd.options.display.max_rows = None

pd.options.display.max_columns = None

# Create playoff test dataset from season averages
@st.cache
def Score_Predictor(home_team, away_team):
    team1 = home_team
    team2 = away_team
    
    team1_data = model_data[com_data['Team'] == team1].drop('TmScore', axis=1).reset_index(drop=True)
    team2_data = model_data[com_data['Team'] == team2].drop('TmScore', axis=1).reset_index(drop=True)
    
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
    
    scores = models[selected_model]['load'].predict(X_Playoff_test)
    #print(team1, "will score", round(scores[0], 1))
    #print(team2, "will score", round(scores[1], 1))
    
    if scores[0] > scores[1]:
        winner = team1
    else:
        winner = team2
    
    #scores_str = f'{scores[0]} vs. {scores[1]}'
    #print(winner, "are the WINNERS!!!")
    
    return scores, winner

# Web scraping of NFL player stats
@st.cache
def load_data(team): #year,
    url = "https://www.pro-football-reference.com/teams/" + teams_dict[selected_team]['Abbrev'].lower() + "/2021.htm"
    df = pd.read_html(url, header = 1)
    df = df[1]
    return df
teamstats = load_data(selected_team) #selected_year, 

st.header('Display 2021 Season Schedule, Results, and Statistics')
st.subheader('Current Team Selection: ' + selected_team)
st.image(teams_dict[selected_team]['Logo'], width = 500)
st.dataframe(teamstats)
st.write("Source: https://www.pro-football-reference.com/teams/" + f"{teams_dict[selected_team]['Abbrev'].lower()}" + "/2021.htm")

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href
st.markdown(filedownload(teamstats), unsafe_allow_html=True)

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


st.subheader(" ")
st.header(f"{selected_team}' Playoff Picture")
st.write(teams_dict[selected_team]['Blurb'])
st.write('Source: https://www.sportingnews.com/us/nfl/news/nfl-playoffs-2022-picks-predictions-bracket-super-bowl/qm7ljbia21w514pj03zl2fvtr')

st.markdown('---')
st.title("Road to Super Bowl LVI")


button1 = st.button("Run Praedico")
col1, col2 = st.columns(2)
col1.title("Wild Card Round")

col1.subheader("AFC Game 1")
col1.image(teams_dict['Kansas City Chiefs']['Logo'], width = 200)
col1.image(teams_dict['Pittsburgh Steelers']['Logo'], width = 200)
col1.subheader("AFC Game 2")
col1.image(teams_dict['Buffalo Bills']['Logo'], width = 200)
col1.image(teams_dict['New England Patriots']['Logo'], width = 200)
col1.subheader("AFC Game 3")
col1.image(teams_dict['Cincinnati Bengals']['Logo'], width = 200)
col1.image(teams_dict['Las Vegas Raiders']['Logo'], width = 200)
col1.subheader("NFC Game 1")
col1.image(teams_dict['Tampa Bay Buccaneers']['Logo'], width = 200)
col1.image(teams_dict['Philadelphia Eagles']['Logo'], width = 200)
col1.subheader("NFC Game 2")
col1.image(teams_dict['Dallas Cowboys']['Logo'], width = 200)
col1.image(teams_dict['San Francisco 49ers']['Logo'], width = 200)
col1.subheader("NFC Game 3")
col1.image(teams_dict['Los Angeles Rams']['Logo'], width = 200)
col1.image(teams_dict['Arizona Cardinals']['Logo'], width = 200)
col1.subheader("AFC Bye Team ")
col1.image(teams_dict['Tennessee Titans']['Logo'], width = 200)
col1.subheader("NFC Bye Team ")
col1.image(teams_dict['Green Bay Packers']['Logo'], width = 200)
container = st.container()

afc_lowest = ''
afc_team1 = ''
afc_team2 = ''

nfc_lowest = ''
nfc_team1 = ''
nfc_team2 = ''

winner = ""

if button1:  
    scores1, afc_winner1 = Score_Predictor('Kansas City Chiefs', 'Pittsburgh Steelers')
    scores2, afc_winner2 = Score_Predictor('Buffalo Bills', 'New England Patriots')
    scores3, afc_winner3 = Score_Predictor('Cincinnati Bengals', 'Las Vegas Raiders')
    scores4, nfc_winner1 = Score_Predictor('Tampa Bay Buccaneers', 'Philadelphia Eagles')
    scores5, nfc_winner2 = Score_Predictor('Dallas Cowboys', 'San Francisco 49ers')
    scores6, nfc_winner3 = Score_Predictor('Los Angeles Rams', 'Arizona Cardinals')
    
    col2.title("Praedico")
    col2.subheader("AFC Game 1 Winner")
    col2.image(teams_dict[afc_winner1]['Logo'], width = 325, caption = f' Final Score: {scores1[0]: .0f} vs. {scores1[1]: .0f}')
    col2.subheader("AFC Game 2 Winner")
    col2.image(teams_dict[afc_winner2]['Logo'], width = 325, caption = f'Final Score: {scores2[0]: .0f} vs. {scores2[1]: .0f}')
    col2.subheader("AFC Game 3 Winner")
    col2.image(teams_dict[afc_winner3]['Logo'], width = 325, caption = f'Final Score: {scores3[0]: .0f} vs. {scores3[1]: .0f}')
    col2.subheader("NFC Game 1 Winner")
    col2.image(teams_dict[nfc_winner1]['Logo'], width = 325, caption = f'Final Score: {scores4[0]: .0f} vs. {scores4[1]: .0f}')
    col2.subheader("NFC Game 2 Winner")
    col2.image(teams_dict[nfc_winner2]['Logo'], width = 325, caption = f'Final Score: {scores5[0]: .0f} vs. {scores5[1]: .0f}')
    col2.subheader("NFC Game 3 Winner")
    col2.image(teams_dict[nfc_winner3]['Logo'], width = 325, caption = f'Final Score: {scores6[0]: .0f} vs. {scores6[1]: .0f}')
    col2.subheader("AFC Bye Team ")
    col2.image(teams_dict['Tennessee Titans']['Logo'], width = 300)
    col2.subheader("NFC Bye Team ")
    col2.image(teams_dict['Green Bay Packers']['Logo'], width = 300)
       
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

    
    st.markdown('---')
    col1, col2 = st.columns(2)
    col1.title("Divisional Round")
    col1.subheader("AFC Divisional Game 1")
    col1.image(teams_dict['Tennessee Titans']['Logo'], width = 200)
    col1.image(teams_dict[afc_lowest]['Logo'], width = 200)

    col1.subheader("AFC Divisional Game 2")
    col1.image(teams_dict[afc_team1]['Logo'], width = 200)
    col1.image(teams_dict[afc_team2]['Logo'], width = 200)

    col1.subheader("NFC Divisional Game 1")
    col1.image(teams_dict['Green Bay Packers']['Logo'], width = 200)
    col1.image(teams_dict[nfc_lowest]['Logo'], width = 200)

    col1.subheader("NFC Divisional Game 2")
    col1.image(teams_dict[nfc_team1]['Logo'], width = 200)
    col1.image(teams_dict[nfc_team2]['Logo'], width = 200)
    
    scores7, winner7 = Score_Predictor('Tennessee Titans', afc_lowest)
    scores8, winner8 = Score_Predictor(afc_team1, afc_team2)
    scores9, winner9 = Score_Predictor('Green Bay Packers', nfc_lowest)
    scores10, winner10 = Score_Predictor(nfc_team1, nfc_team2)
   
    col2.title("Praedico")  
    col2.subheader("AFC Divisional Game 1 Winner")
    col2.image(teams_dict[winner7]['Logo'], width = 350, caption = f'Final Score: {scores7[0]: .0f} vs. {scores7[1]: .0f}')

    col2.subheader("AFC Divisional Game 2 Winner")
    col2.image(teams_dict[winner8]['Logo'], width = 350, caption = f'Final Score: {scores8[0]: .0f} vs. {scores8[1]: .0f}')

    col2.subheader("NFC Divisional Game 1 Winner")
    col2.image(teams_dict[winner9]['Logo'], width = 350, caption = f'Final Score: {scores9[0]: .0f} vs. {scores9[1]: .0f}')

    col2.subheader("NFC Divisional Game 2 Winner")
    col2.image(teams_dict[winner10]['Logo'], width = 350, caption = f'Final Score: {scores10[0]: .0f} vs. {scores10[1]: .0f}')
        
    st.markdown('---')
    col1, col2 = st.columns(2)
    col1.title("Conference Championships")
    col1.subheader("AFC Final Game")
    col1.image(teams_dict[winner7]['Logo'], width = 200)
    col1.image(teams_dict[winner8]['Logo'], width = 200)

    col1.subheader("NFC Final Game")
    col1.image(teams_dict[winner9]['Logo'], width = 200)
    col1.image(teams_dict[winner10]['Logo'], width = 200)

    scores11, winner11 = Score_Predictor(winner7, winner8)
    scores12, winner12 = Score_Predictor(winner9, winner10)

    col2.title("Praedico")
    col2.subheader("AFC Final Winner")
    col2.image(teams_dict[winner11]['Logo'], width = 400, caption = f'Final Score: {scores11[0]: .0f} vs. {scores11[1]: .0f}')
            
    col2.subheader("NFC Final Winner")
    col2.image(teams_dict[winner12]['Logo'], width = 400, caption = f'Final Score: {scores12[0]: .0f} vs. {scores12[1]: .0f}')
               
    st.markdown('---')
    col1, col2 = st.columns(2)
    col1.title("Super Bowl")
    col1.image(teams_dict[winner11]['Logo'], width = 200)
    col1.image(teams_dict[winner12]['Logo'], width = 200)

    col2.title("Super Bowl Winner")
    scores13, winner13 = Score_Predictor(winner11, winner12)
          
    col2.image(teams_dict[winner13]['Logo'], width = 600, caption = f'Final Score: {scores13[0]: .0f} vs. {scores13[1]: .0f}')

st.sidebar.header('Create Your Own Game!')   
selected_team1 = st.sidebar.selectbox("Home Teams", sorted_unique_team)
selected_team2 = st.sidebar.selectbox("Away Teams", sorted_unique_team, index=1)

st.markdown('---')
st.markdown('---')
col1, col2 = st.columns(2)
col1.subheader("Single Game Matchup")
col1.image(teams_dict[selected_team1]['Logo'], width = 200)
col1.text("  ")
col1.image(teams_dict[selected_team2]['Logo'], width = 200)

button1 = st.sidebar.button("Show me the result using Praedico")
if button1:  
    scores, winner = Score_Predictor(selected_team1, selected_team2)
    
    col2.subheader("Single Match Playoff")
    col2.image(teams_dict[winner]['Logo'], width = 400, caption = f'Final Score: {scores[0]: .0f} vs. {scores[1]: .0f}')