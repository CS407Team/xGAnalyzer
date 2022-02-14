import json
import requests

with open("team_standings") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

file = open("team_data", "a")

url = "https://api-football-v1.p.rapidapi.com/v3/teams"


for index in jsonObject:
    querystring = {"id":index["team"]["id"]}
    headers = {
	    'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
	    'x-rapidapi-key': "f6a74521femsh3da9a6c760ad94dp1ff3e9jsn7e739e41cf69"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data_json = json.loads(response.text)
    data_dictionary = data_json["response"]
    data = data_dictionary[0]
    str = json.dumps(data)
    file.write(str)
    file.write("\n")

file.close()


