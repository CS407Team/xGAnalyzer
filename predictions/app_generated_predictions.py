import json

from flask_login import current_user

from app.models import SeasonTable, TablePredictions, Teams
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
    # with open(filepath, "w") as outfile:
    with open("app/exports/app_preds/application_table_pred.json", "w") as outfile:
        print(outfile.name)
        json.dump(predictionary, outfile, indent=2)
    return filepath


def export_with_compare(prediction_name):
    prediction = TablePredictions.query.filter_by(userid=current_user.userid, name=prediction_name).first()
    print(prediction.name)
    filepath = f'exports\\app_preds\\application_table_pred_compare.txt'
    app_pred = SeasonTable.query.filter_by(round_number=38, team_id=prediction.team_id).order_by(
        'team_position').first()
    team = Teams.query.filter_by(team_id=prediction.team_id).first()
    with open("app/exports/app_preds/application_table_pred_compare.txt", "w") as outfile:
        outfile.write(f'Team Name: {team.team_name}\n')
        outfile.write(f'Your Prediction: Position {prediction.team_position}\n')
        outfile.write(f'Application\'s Prediction: Position {app_pred.team_position}\n')
        outfile.close()
    return filepath
