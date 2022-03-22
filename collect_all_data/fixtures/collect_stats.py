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

# team = "Liverpool"
# away = "Manchester United"
round = ""
count = 0
file = open("file2.csv","a")

for curr_fixture in jsonObject:
#    print(curr_fixture['fixture']['id'])
   count = count +1

print(count)
                    
    
    

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

