from os import walk

file1 = open('../results1.txt', 'r')
Lines = file1.readlines()
results = []
mypath = "C:\\Users\\Downloads\\laliga"
filenames = next(walk(mypath), (None, None, []))[2]
i = 0
teams = ["La Liga", "Rayo Vallecano", "Celta Vigo", "Granada", "Athletic Bilbao", "Cadiz", "Osasuna", "Barcelona",
         "Elche", "Real Madrid", "Getafe", "Deportivo", "Betis", "Mallorca", "Real Sociedad", "Villarreal", "Espanyol",
         "Valencia","Levante", "Atletico","Sevilla"]

if __name__ == '__main__':
    print(str(teams.index("Valencia")+100))
    for i in range(len(Lines) - 3):
        if i >= 3 and (i - 3) % 7 == 0:
            if (i - 3) % 700 == 0:
                print(str(Lines[i]))
            result = []
            home = str(Lines[i]).replace('   "name": "', '').replace('",', '')
            home = home[0:len(home) - 1]
            if home == "CÃ¡diz":
                home = "Cadiz"
            elif home == "AlavÃ©s":
                home = "Deportivo"
            elif home == "AtlÃ©tico Madrid":
                home = "Atletico"
            elif home == "Athletic Club":
                home = "Athletic Bilbao"
            result.append(home)
            away = str(Lines[i + 1]).replace('   "awayteam": "', '').replace('",', '')
            away = away[0:len(away) - 1]
            if away == "CÃ¡diz":
                away = "Cadiz"
            elif away == "AlavÃ©s":
                away = "Deportivo"
            elif away == "AtlÃ©tico Madrid":
                away = "Atletico"
            elif away == "Athletic Club":
                away = "Athletic Bilbao"
            result.append(away)
            score = str(Lines[i + 3]).replace('   "result": "', '').replace('",', '')
            if (i - 3) % 700 == 0:
                print(str(score))
            homescore = score.split("â€“")[0]
            awayscore = score.split("â€“")[1]
            awayscore = awayscore[0:len(awayscore) - 1]
            result.append(homescore)
            result.append(awayscore)
            results.append(result)
    print(results[0])
    insert = str("INSERT" + " INTO new_stats(home_team_id,away_team_id,home_goals,away_goals) VALUES ")
    for res in results:
        insert += "("
        insert += str(teams.index(res[0])+100)
        insert += ","
        insert += str(teams.index(res[1])+100)
        insert += ","
        insert += res[2]
        insert += ","
        insert += res[3]
        insert += "),"
    insert = insert[0:len(insert) - 1] + ";"
    update = ""
    print(insert)
