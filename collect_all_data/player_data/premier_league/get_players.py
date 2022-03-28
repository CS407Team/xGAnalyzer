import requests
import json

url = "https://api-football-v1.p.rapidapi.com/v3/players"
teams = [
    {"id":"50","team":"Manchester City"},
    {"id":"40", "team": "Liverpool"},
    {"id":"49", "team": "Chelsea"},
    {"id":"48", "team": "West Ham"},
    {"id":"33", "team": "Manchester United"},
    {"id":"42", "team": "Arsenal"},
    {"id":"39", "team": "Wolves"},
    {"id":"47", "team": "Tottenham"},
    {"id":"51", "team": "Brighton"},
    {"id":"41", "team": "Southampton"},
    {"id":"46", "team": "Leicester"},
    {"id":"66", "team": "Aston Villa"},
    {"id":"52", "team": "Crystal Palace"},
    {"id":"55", "team": "Brentford"},
    {"id":"63", "team": "Leeds"},
    {"id":"45", "team": "Everton"},
    {"id":"34", "team": "Newcastle"},
    {"id":"71", "team": "Norwich"},
    {"id":"38", "team": "Watford"},
    {"id":"44", "team": "Burnley"},
]

for team in teams:
    id = team["id"]
    file = open(team["team"],"a")
    querystring = {"team":id,"season":"2020"}

    headers = {
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com",
        "X-RapidAPI-Key": "f6a74521femsh3da9a6c760ad94dp1ff3e9jsn7e739e41cf69"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data_json = json.loads(response.text)
    json.dump(data_json["response"], file)
    file.close()