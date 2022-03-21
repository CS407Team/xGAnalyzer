import requests
import json

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

# leagues = ["premier_league", "bundesliga","laliga","ligue1","serie_a"]

# seasons = ["2021","2020","2019","2018", "2017","2016"]
# seasons1= ["2015","2014","2013","2012","2011","2010"]


headers = {
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
    'x-rapidapi-key': "f6a74521femsh3da9a6c760ad94dp1ff3e9jsn7e739e41cf69"
    }

# for season in seasons1:
querystring = {"league":"61","season":"2015"}

response = requests.request("GET", url, headers=headers, params=querystring)
response_dictionary = json.loads(response.text)
file_name = "ligue1/2015"
file = open(file_name,"a")
file.write(json.dumps(response_dictionary["response"]))
file.close()   