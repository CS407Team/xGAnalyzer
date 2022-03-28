import json
from urllib.request import HTTPPasswordMgrWithPriorAuth


def collect_fixure(team1, team2):

    # seasons = ["2021","2020","2019","2018","2017","2016","2015","2015","2014","2013","2012","2011","2010"]
    seasons = ["2021","2020","2019","2018","2017","2016"]

    # for season in seasons:
    # filename = "premier_league/"+season
    filename = "2021"
    with open(filename) as jsonFile:
        jsonObject = json.load(jsonFile)
    jsonFile.close()

    print("Home: ", team1, "Away: ", team2)
    team = team1
    away = team2
    round = ""
    count = 0
    file = open("fixture_data.csv","a")
    file.write("RoundNum,HalftimeHome,HalftimeAway,FulltimeHome,FulltimeAway,Winner\n")

    for curr_fixture in jsonObject:
        if(str(curr_fixture['fixture']['status']['long']) == "Not Started" and curr_fixture['fixture']['status']['elapsed'] == None):
            teams = {"home":str(curr_fixture['teams']['home']['name']), "away":str(curr_fixture['teams']["away"]['name'])}        
            # print(teams)
            for season in seasons[1:]:
                next_season = season
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
    print("Data collection status: COMPLETE")

