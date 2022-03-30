import pandas
import math
import json


from sklearn.preprocessing import StandardScaler


def find_team(team):
    index = 0
    for current_team in possession['Unnamed: 0']:
        if current_team == stats["team"]:
            return index
        index = index+1
        
    return -1

# Get teams
teams = []
file = open("../../../data_files/team_data","r")
lines = file.readlines()

for line in lines:
    data = json.loads(line.strip())
    team_name = data["team"]["name"]
    team_id = data["team"]["id"]
    team = {"team":team_name, "id":team_id}
    teams.append(team)    



print("\n\n\n")

# def generate_stats(team):

standings = pandas.read_csv("team_standings.csv")
defense = pandas.read_csv("defense.csv")
basic_goalkeeping = pandas.read_csv("basic_goalkeeping.csv")
advanced_goalkeeping = pandas.read_csv("advanced_goalkeeping.csv")
bookings = pandas.read_csv("bookings.csv")
pass_types = pandas.read_csv("pass_types.csv")
possession = pandas.read_csv("possession.csv")
shooting = pandas.read_csv("shooting.csv")
standard = pandas.read_csv("standard_stats.csv")
passing = pandas.read_csv("passing.csv")
shots = pandas.read_csv("shots.csv")



stats = {}
round_stats = []
# team = "Manchester City"

for current_team in teams:
    
    
    stats["team"] = current_team['team']
    stats["id"] = current_team['id']
    index = find_team(current_team)

    # Generate Possession
    # print(possession.columns)
    
    games_played = int(str(possession['Unnamed: 1'][index]))
    current_possession = float(str(possession['Unnamed: 2'][index]))
    projected_possession = (current_possession * games_played)/(games_played+1)
    stats['possession'] = projected_possession
    # print("Projected Possession: %.1f" % projected_possession)

    # Generate Total Shots
    # print(shots.columns)
    current_total_shots = float(str(shots['SCA.1'][index]))
    projected_shots = math.floor((current_total_shots * games_played)/(games_played))
    stats['total_shots'] = projected_shots
    # print("Projected Total Shots: ", projected_shots)

    # Generate Shots on target
    on_target = math.ceil((float(str(shooting['Standard.3'][index]))/100) * projected_shots)
    stats['on_target'] = on_target
    # print("Projected Shots on Target: ", on_target)

    # Generate Red Cards
    red_cards = math.floor(float(str(standard['Performance.6'][index]))/games_played)
    stats['red_cards'] = red_cards
    # print("Projected Red Cards: ", red_cards)

    # Generate Yellow Cards
    yellow_cards = math.ceil(float(str(standard['Performance.5'][index]))/games_played)
    stats['yellow_cards'] = yellow_cards
    # print("Projected Yellow Cards: ", yellow_cards)


    # Generate Penalties
    penalties = math.floor(float(str(standard['Performance.3'][index]))/games_played)
    stats['penalties'] = penalties
    # print("Projected Penalties: ", penalies)

    # Generate Freekicks
    freekicks = math.ceil((int(str(pass_types['Pass Types.2'][index])) + int(str(shooting['Standard.9'][index])))/games_played)
    stats['freekicks'] = freekicks
    # print("Projected Freekicks: ", freekicks)

    # Generate Total Attempted Passes
    total_passes = int(float(str(passing['Total.1'][index]))/games_played)
    stats['total_passes'] = total_passes
    # print("Projected Total Passes: ", total_passes)

    # Generate Completed Passes
    complete_passes = int((float(str(passing['Total.2'][index]))/100) * total_passes)
    stats['complete_passes'] = complete_passes
    # print("Projected Complete Passes: ", complete_passes)

    round_stats.append(stats)
    # print(stats)

print(round_stats)