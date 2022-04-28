from os import walk
import teams
file1 = open('../results1.txt', 'r')
Lines = file1.readlines()
results = []
result = []
mypath = "C:\\Users\\Downloads\\laliga"
filenames = next(walk(mypath), (None, None, []))[2]
i = 0
tms = ['Premier League', 'Manchester City', 'Liverpool', 'Chelsea', 'West Ham', 'Manchester Utd',
         'Arsenal', 'Wolves',
         'Tottenham', 'Brighton', 'Southampton', 'Leicester City', 'Aston Villa', 'Crystal Palace', 'Brentford',
         'Leeds United', 'Everton', 'Newcastle Utd', 'Norwich City', 'Watford', 'Burnley',
         "La Liga", "Rayo Vallecano", "Celta Vigo", "Granada", "Athletic Bilbao", "Cadiz", "Osasuna", "Barcelona",
         "Elche", "Real Madrid", "Getafe", "Deportivo", "Betis", "Mallorca", "Real Sociedad", "Villarreal", "Espanyol",
         "Valencia", "Levante", "Atletico", "Sevilla"]
j = 0
if __name__ == '__main__':
    set1 = set(teams.teams_2017)
    set2 = set(teams.teams_2021)
    print(set1-set2)
    for i in range(len(Lines) - 3):
        if str(Lines[i]).__contains__("name"):
            home = str(Lines[i]).replace('   "name": "', '').replace('",', '')
            home = home[0:len(home) - 2]
            away = home
            if home == "Bournemouth":
                away = "Leeds United"
            elif home == "Huddersfield":
                away = "Brentford"
            elif home == "West Brom":
                away = "Norwich City"
            elif home == "Fulham":
                away = "Aston Villa"
            elif home == "Sheffield Utd":
                away = "Wolves"
            results.append(away)
            result.append(home)
    print(str(result))
    insert = str("INSERT" + " INTO positions VALUES ")
    for i in range(len(results)):
        insert += "("
        insert += "2021"
        insert += ","
        insert += str(i+1)
        insert += ","
        insert += str(i+1)
        insert += "),"
    insert = insert[0:len(insert) - 1] + ";"
    update = ""
    print(insert)
