import requests
import json
import csv

def get_leagues():
    url = "https://api-football-v1.p.rapidapi.com/v3/leagues"
    querystring = {"id":"39"}
    # laliga = {"id":"140"}
    # bundesliga = {"id":"78"}
    # ligue = {"id":"61"}
    # seriea = {"id":"135"}
    # leagues = [premier_league, laliga,bundesliga, ligue, seriea]
    # for querystring in leagues:
    headers = {
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
        'x-rapidapi-key': "f6a74521femsh3da9a6c760ad94dp1ff3e9jsn7e739e41cf69"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    response_dictionary = json.loads(response.text)
    values = json.dumps(response_dictionary["response"][0])
    print(type(values))
    file = open("league_info.json", "a")
    file.write(values)
    # league_data = (response_dictionary["response"])
    # print(league_data[0]["league"]["name"])
    # print(league_data[0]["league"]["type"])
    # print(league_data[0]["country"]["name"])
    file.close()
      

def get_teams(team_ids, league_id):
    file = open("team_data", "a")
    querystring = {"season":"2021","league":"39"}
    # for querystring in team_ids:
    url = "https://api-football-v1.p.rapidapi.com/v3/teams"
    headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': "f6a74521femsh3da9a6c760ad94dp1ff3e9jsn7e739e41cf69"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    teams_result = json.loads(response.text)
    teams_dictionary = teams_result["response"]
    team_data =  json.dumps(teams_dictionary[0])
    file.write(team_data)
    players("39")
    file.close()
        
def get_team_data():
        url = "https://api-football-v1.p.rapidapi.com/v3/standings"
        premier_league = {"season":"2021","league":"39"}
        laliga = {"season":"2021","league":"140"}
        bundesliga = {"season":"2021","league":"78"}
        ligue1 = {"season":"2021","league":"61"}
        seriea = {"season":"2021","league":"135"}
        
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': "f6a74521femsh3da9a6c760ad94dp1ff3e9jsn7e739e41cf69"
        }
        
        # leagues = [premier_league, laliga,bundesliga, ligue1, seriea]
        # for querystring in leagues:
        response = requests.request("GET", url, headers=headers, params=premier_league)
        standing_result = json.loads(response.text)
        standing_dictionary = standing_result["response"]
        teams = standing_dictionary[0]["league"]["standings"][0]
        team_ids=[]
        for team in teams:
                team_ids.append({ "id":team["team"]["id"]})
        get_teams(premier_league,39)
        
        
def players(team_id):
        file = open("players", "a")
        url = "https://api-football-v1.p.rapidapi.com/v3/players"
        querystring = {"team":team_id,"season":"2021"}
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': "f6a74521femsh3da9a6c760ad94dp1ff3e9jsn7e739e41cf69"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        player_result = json.loads(response.text)
        players = json.dumps(player_result["response"])
        file.write(players)
        file.close()
                
def main():
    get_leagues()
    get_team_data()

if __name__ == "__main__":
    main()
