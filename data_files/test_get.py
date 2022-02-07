import requests
import pandas as pd
import json


url = "https://api-football-v1.p.rapidapi.com/v3/leagues"
querystring = {"id":"39"}

headers = {
'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
    'x-rapidapi-key': "f6a74521femsh3da9a6c760ad94dp1ff3e9jsn7e739e41cf69"
}
response = requests.request("GET", url, headers=headers, params=querystring)
response_dictionary = json.loads(response.text)

#print(response.text)
values = json.dumps(response_dictionary["response"][0])
print(type(values))
file = open("data.json", "a")
file.write(values)
file.close()


