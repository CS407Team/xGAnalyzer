import json
import pandas
import math


# dict_keys(['team', 'league', 'games', 'substitutes', 'shots', 'goals', 'passes', 'tackles', 'duels', 'dribbles', 'fouls', 'cards', 'penalty'])
combined_xg = []
teams = [
    {"id":"50","team":"Manchester City"},
    {"id":"40", "team": "Liverpool"},
    {"id":"49", "team": "Chelsea"},
    {"id":"48", "team": "West Ham"},
    {"id":"33", "team": "Manchester United"},
    {"id":"42", "team": "Arsenal"},
    {"id":"39", "team": "Wolves"},
    {"id":"47", "team": "Tottenham"},
    {"id":"51", "team": "Brighton"},
    {"id":"41", "team": "Southampton"},
    {"id":"46", "team": "Leicester"},
    {"id":"66", "team": "Aston Villa"},
    {"id":"52", "team": "Crystal Palace"},
    {"id":"55", "team": "Brentford"},
    {"id":"63", "team": "Leeds"},
    {"id":"45", "team": "Everton"},
    {"id":"34", "team": "Newcastle"},
    {"id":"71", "team": "Norwich"},
    {"id":"38", "team": "Watford"},
    {"id":"44", "team": "Burnley"},
]


file = open("teams_list","r")
lines = file.readlines()
team_files = []

player_stats = open("player_stats","a")

for line in lines:
    data = line.strip()
    team_files.append(data)

for team in teams:
    file = open(team["team"],"r")
    files_lines = file.readlines()
    players = []
    # team_name = team["team"] +"_xg"
    # team_xg = open(team_name,"a")
    
    print(team["team"]+"\n\n")
    for current_line in files_lines:
        players = json.loads(current_line.strip())
        # print("\n\n\n")
        # players.append(data) 
             
    # print(len(players))
    
        for player in players:
            
            team_id = player["statistics"][0]["team"]["id"]
            
            player_id = player["player"]['id']
            player_name = player["player"]['name']
            games = 1
            if( player["statistics"][0]['games']['appearences']!= None):
                games = player["statistics"][0]['games']['appearences']
            
            minutes = 0
            if(player["statistics"][0]['games']['minutes'] != None):
                minutes = int(player["statistics"][0]['games']['minutes'])
                
            rating = 0
            if(player["statistics"][0]['games']['rating'] != None):
                rating = player["statistics"][0]['games']['rating']
            
            
            total_shots = 0
            if(player["statistics"][0]['shots']['total'] != None):
                total_shots = player["statistics"][0]['shots']['total']
                
            on_target = 0
            if(player["statistics"][0]['shots']['on'] != None):
                on_target = player["statistics"][0]['shots']['on']
                
            total_goals = 0
            if(player["statistics"][0]['goals']['total'] != None):
                total_goals = player["statistics"][0]['goals']['total']
                
            conceded = 0
            if(player["statistics"][0]['goals']['conceded'] != None):
                conceded = player["statistics"][0]['goals']['conceded']
                
            assists = 0
            if(player["statistics"][0]['goals']['assists'] != None):
                assists = player["statistics"][0]['goals']['assists']
                
            saves = 0
            if(player["statistics"][0]['goals']['saves'] != None):
                saves = player["statistics"][0]['goals']['saves']
                
            total_passes  = 0
            if(player["statistics"][0]['passes']['total'] != None):
                total_passes = player["statistics"][0]['passes']['total']
                
            complete = 0
            if(player["statistics"][0]['passes']['accuracy'] != None):
                complete = int(float(player["statistics"][0]['passes']['accuracy']/100) * total_passes)
                
            total_tackles = 0
            if(player["statistics"][0]['tackles']['total']!= None):
                total_tackles = player["statistics"][0]['tackles']['total']
                
            total_duels = 0
            if(player["statistics"][0]['duels']['total'] != None):
                total_duels = player["statistics"][0]['duels']['total']
                
            duels_won = 0
            if(player["statistics"][0]['duels']['won'] != None):
                duels_won = player["statistics"][0]['duels']['won']
            
            attempted_dribbles = 0
            if(player["statistics"][0]['dribbles']['attempts'] != None):
                attempted_dribbles = player["statistics"][0]['dribbles']['attempts']
                
            successful_dribbles = 0
            if(player["statistics"][0]['dribbles']['success'] != None):
                successful_dribbles = player["statistics"][0]['dribbles']['success']
                
            total_fouls = 0
            if(player["statistics"][0]['fouls']['committed']!= None):
                total_fouls = player["statistics"][0]['fouls']['committed']
        
            red_cards = 0
            if(player["statistics"][0]['cards']['yellow']!=None):
                red_cards = player["statistics"][0]['cards']['yellow']
                
            yellow_cards = 0
            if(player["statistics"][0]['cards']['red'] != None):
                yellow_cards = player["statistics"][0]['cards']['red']
            
            
            red_cards = 0
            if(player["statistics"][0]['cards']['yellow'] != None):
                red_cards = player["statistics"][0]['cards']['yellow']
                
            penalties = 0
            if(player["statistics"][0]['penalty']['scored'] != None):
                penalties = player["statistics"][0]['penalty']['scored']
                
            
            rating = 0
            if(player['statistics'][0]['games']['rating']) == None:
                rating = -1
            else:
                rating = player['statistics'][0]['games']['rating']
                
            
            avg_minutes = 0
            next_rating = 0
            avg_shots = 0
            on_target = 0
            avg_conceded = 0
            avg_goals = 0
            avg_assists = 0
            avg_saves = 0
            avg_total_passes = 0
            avg_complete = 0
            avg_yellow = 0
            avg_red = 0
            avg_tackles = 0
            avg_rating = 0
            if games != 0:
                if(minutes != None and games != None):
                    avg_minutes = minutes/games
                    avg_rating = rating
                if(rating != None and games != None):
                    next_rating = (float(rating)*(games))/(games+1)
                if(total_shots != None and games != None):
                    avg_shots = int(total_shots/games)
                    
                if(on_target != None and games != None):
                    on_target = math.floor(on_target/games)
                    
                if(conceded != None and games != None):
                    avg_conceded = conceded/games
                    
                if(total_goals != None and games != None):
                    avg_goals =math.ceil(total_goals/games)
                    print(total_goals)
                    
                if(assists != None and games != None):
                    avg_assists = math.floor(assists/games)
                    
                if(saves != None):
                    avg_saves = math.ceil(saves/games)
            
                if(total_passes != None and games != None):
                    avg_total_passes = math.ceil(total_passes/games)
                        
                if(complete != None):
                    avg_complete = math.ceil(complete/games)
                    
                if(yellow_cards != None):
                    avg_yellow = math.ceil(yellow_cards/games)
                    
                if red_cards != None:
                    avg_red = math.floor(red_cards/games)

                if total_tackles != None:
                    avg_tackles = math.ceil(total_tackles/games)

                
            
            player_xg = {"id":player_id, 
                        "name":player_name, 
                        "avg_minutes":int(avg_minutes), 
                        "avg_shots":avg_shots,
                        "avg_target":on_target,
                        "avg_conceded":avg_conceded,
                        "avg_goals":avg_goals,
                        "avg_assists":avg_assists,
                        "avg_saves":avg_saves,
                        "avg_total_passes":avg_total_passes,
                        "avg_complete":avg_complete,
                        "avg_yellow":avg_yellow,
                        "avg_red":avg_red,
                        "avg_tackles":avg_tackles,
                        "avg_rating":avg_rating,
                        "team_id":team_id
                        }
            # combined_xg.append(player_xg)  
            # print (player["player"]['name'])    
            # print(player_xg)
            # print("\n\n")
            print(player_xg)
            # combined_xg.append(player_xg)
        #     player_xg = {}
            json.dump(player_xg,player_stats)
            player_stats.write("\n")
        #     team_xg.write("\n")
        # team_xg.close()

            # print( player["player"])
        # print(combined_xg)
player_stats.close()
        
        
# get_stats(29)
# # get_stats(30)
# # get_stats(31)
# # get_stats(32)
# # get_stats(33)
# # get_stats(34)
# # get_stats(35)
# # get_stats(36)
# # get_stats(37)
# # get_stats(38)