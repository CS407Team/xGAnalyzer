import json

def contains_team(team, teams):
    if(teams["home"] == team or teams["away"] == team):
        return True
    return False

def get_remaining_fixtures(team):
    filename = "2021"
    with open(filename) as jsonFile:
        jsonObject = json.load(jsonFile)
    jsonFile.close()
    
    fixtures_to_play = []
    round_num = 0

    for curr_fixture in jsonObject:
        if(str(curr_fixture['fixture']['status']['long']) == "Not Started" and curr_fixture['fixture']['status']['elapsed'] == None):
            teams = {"home":str(curr_fixture['teams']['home']['name']), "away":str(curr_fixture['teams']["away"]['name'])}         
            if(contains_team(team, teams)):
                round = str(curr_fixture['league']['round'])
                if(round_num == 0):
                    round_num = round.split(" - ")[1]
                fixtures_to_play.append(teams)
    
    return {"round": round_num, "fixtures":fixtures_to_play}