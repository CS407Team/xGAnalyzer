import json
from urllib.request import HTTPPasswordMgrWithPriorAuth

# seasons = ["2021","2020","2019","2018","2017","2016","2015","2015","2014","2013","2012","2011","2010"]
seasons = ["2021","2020","2019","2018","2017","2016"]

# for season in seasons:
# filename = "premier_league/"+season
filename = "premier_league/2021"
with open(filename) as jsonFile:
    jsonObject = json.load(jsonFile)
jsonFile.close()

team = "Liverpool"
away = "Manchester United"
round = ""
count = 0
file = open("file2.csv","a")

for curr_fixture in jsonObject:
    if(str(curr_fixture['fixture']['status']['long']) == "Not Started" and curr_fixture['fixture']['status']['elapsed'] == None):
        teams = {"home":str(curr_fixture['teams']['home']['name']), "away":str(curr_fixture['teams']["away"]['name'])}        
        # print(teams)
        for season in seasons[1:]:
            next_season = "premier_league/"+season
            with open(next_season) as seasonFile:
                seasonObject = json.load(seasonFile)
            seasonFile.close()
            
            for fixureObject in seasonObject:
                fixure_teams = fixureObject["teams"]
                if(str(fixure_teams["home"]["name"]) == team and fixure_teams["away"]["name"] == away):
                    round = str(fixureObject['league']['round'])
                    num = round.split(" - ")[1]
                    winner = ""
                    half_time_home = fixureObject['score']['halftime']['home']
                    half_time_away = fixureObject['score']['halftime']['away']
                    full_time_home = fixureObject['score']['fulltime']['home']
                    full_time_away = fixureObject['score']['fulltime']['away']
                    if(bool(fixure_teams['home']['winner']) == True):
                        winner = fixure_teams['home']['id']
                    elif(bool(fixure_teams['away']['winner']) == True):
                        winner = fixure_teams['away']['id']
                    else:
                        winner = "0"
                    line = str(num)+","+ str(half_time_away)+","+str(half_time_home)+","+ str(full_time_away)+","+ str(full_time_home)+","+ str(winner)+"\n"
                    # print(line)
                    file.write(line)
file.close()
                    
    
    

# round = "32"
# teams = {}

# for object in jsonObject:
#     current_teams = object["teams"]

#     if round in object["league"]["round"]:
#         # print(object["teams"])
#         if(str(current_teams["home"]['name']) == team or str(current_teams["away"]['name']) == team):
#             teams = {"home":str(current_teams['home']['name']), "away":str(current_teams["away"]['name'])}
#             print (object['score'])
#             break
                    

# for season in seasons[1:]:
#     next_season = "premier_league/"+season
#     with open(next_season) as seasonFile:
#         seasonObject = json.load(seasonFile)
#     seasonFile.close()
    
#     for fixureObject in seasonObject:              
#         fixure_teams = fixureObject["teams"]
#         if(str(fixure_teams["home"]["name"]) == teams["home"] and fixure_teams["away"]["name"] == teams["away"]):
#             print(fixureObject['score'])

