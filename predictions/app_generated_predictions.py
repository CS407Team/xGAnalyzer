import json

from app.models import SeasonTable
from data_files import database


def export():
    data = SeasonTable.query.filter_by(round_number=38).order_by('team_position').all()
    predictionary = []
    for team in data:
        entry = {
            "Team": team.team_id,
            "Position": team.team_position,
            "Points": team.team_points,
            "Games Played": team.games_played,
            "Games Won": team.won,
            "Games Lost": team.lost,
            "Games Drawn": team.drawn
        }
        predictionary.append(entry)
    filepath = f'exports\\app_preds\\application_table_pred.json'
    with open(filepath, "w") as outfile:
    #with open("app/exports/app_preds/application_table_pred.json", "w") as outfile:
        print(outfile.name)
        json.dump(predictionary, outfile, indent=2)
    return filepath
