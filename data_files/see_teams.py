import json

with open("team_standings") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()
    
for index in jsonObject:
    print(index["team"]["id"])
    