import json

file = open("team_data","r")
lines = file.readlines()

count = 0
for line in lines:
    count+= 1
    data = json.loads(line.strip())
    print(data["team"]["name"])
    