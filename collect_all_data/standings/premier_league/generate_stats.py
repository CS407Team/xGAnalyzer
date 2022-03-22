import pandas
import math

from sklearn.preprocessing import StandardScaler


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

team = "Chelsea"
stats = {}

index = 0

# Generate Possession
# print(possession.columns)
for current_team in possession['Unnamed: 0']:
    if current_team == team:
        break
    index = index+1

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
print("Projected Yellow Cards: ", yellow_cards)


# Generate Penalties
penalties = math.floor(float(str(standard['Performance.3'][index]))/games_played)
print("Projected Penalties: ", penalties)

# Generate Freekicks
freekicks = math.ceil((int(str(pass_types['Pass Types.2'][index])) + int(str(shooting['Standard.9'][index])))/games_played)
print("Projected Freekicks: ", freekicks)

# Generate Total Attempted Passes
total_passes = int(float(str(passing['Total.1'][index]))/games_played)
print("Projected Total Passes: ", total_passes)

# Generate Completed Passes
complete_passes = int((float(str(passing['Total.2'][index]))/100) * total_passes)
print("Projected Complete Passes: ", complete_passes)
