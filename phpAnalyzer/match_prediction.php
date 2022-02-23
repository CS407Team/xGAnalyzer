<?php
    include("connect.php");

//     select * from games where hometeam_id = 1 and awayteam_id = 17 and status = 'not_played';
// +--------+---------------+-------------+-------------+----------+-----------+-------------+-----------------+----------------+------------+--------------+
// | gameid | tournament_id | hometeam_id | awayteam_id | stats_id | winner_id | location_id | prediction_name | location       | status     | round_number |
// +--------+---------------+-------------+-------------+----------+-----------+-------------+-----------------+----------------+------------+--------------+
// |    359 |            39 |           1 |          17 |      359 |         0 |        NULL | NULL            | Etihad Stadium | not_played |           36 |
// +--------+---------------+-------------+-------------+----------+-----------+-------------+-----------------+----------------+------------+--------------+
    
    $sql = "select * from teams";
    $query = mysqli_query($conn, $sql);

    echo "
    <!DOCTYPE html>
    <html>
    <style>
    table, th, td {
    border:1px solid black;
    }
    </style>
    <body>";
    

    echo "

        <form method='POST' action='match_prediction.php'>
        <input name='prediction_name' type='text' placeholder='Name of Prediction'/><br/>
        <table>
        <tr>
          <th>Home Team</th>
          <th>Away Team</th>
        </tr>
          <tr>
          <td>
            <select name='home_team'>";

                if(!$query){
                    echo $conn->error;
                }else{
                    while($team = $query->fetch_assoc()){ 
                        $id = $team['team_id'];
                        $tournament_id = $team['tournament_id'];
                        $name = $team['team_name'];
                        echo "<option value='$id'>$name</option>";
                    }
                }

        echo"        
            </select>
            </td>
            <td>
            <select name='away_team'>";

            $query = mysqli_query($conn, $sql);

                if(!$query){
                    echo $conn->error;
                }else{
                    while($team = $query->fetch_assoc()){ 
                        $id = $team['team_id'];
                        $tournament_id = $team['tournament_id'];
                        $name = $team['team_name'];
                        echo "<option value='$id'>$name</option>";
                    }
                }

        echo"
            </td>
            </tr>
            <tr>
                <td> <input type='text' name='home_goals' placeholder='Home Team Goals'/></td>
                <td> <input type='text' name='away_goals' placeholder='Away Teams Goals'/></td>
            </tr>
            <tr>
                <td> <input type='text' name='home_possession' placeholder='Home Possession %'/></td>
                <td> <input type='text' name='away_possession' placeholder='Away Possession %'/></td>
            </tr>
            <tr>
                <td> <input type='text' name='home_shots' placeholder='Home Shots'/></td>
                <td> <input type='text' name='away_shots' placeholder='Away Shots %'/></td>
            </tr>
            <tr>
                <td> <input type='text' name='home_target' placeholder='Shots on Target'/></td>
                <td> <input type='text' name='away_target' placeholder='Shots on Target'/></td>
            </tr>
            <tr>
                <td> <input type='text' name='home_yellow' placeholder='Yellow Cards'/></td>
                <td> <input type='text' name='away_yellow' placeholder='Yellow Cards'/></td>
            </tr>
            <tr>
                <td> <input type='text' name='home_red' placeholder='Red Cards'/></td>
                <td> <input type='text' name='away_red' placeholder='Red Cards'/></td>
            </tr>
            <tr>
                <td> <input type='text' name='home_subs' placeholder='Number Subs'/></td>
                <td> <input type='text' name='away_subs' placeholder='Number Subs'/></td>
            </tr>
            <tr>
                <td> <input type='text' name='home_corners' placeholder='Corner Kicks'/></td>
                <td> <input type='text' name='away_corners' placeholder='Corner Kicks'/></td>
            </tr>
            <tr>
                <td> <input type='text' name='home_pens' placeholder='Penalty Kicks'/></td>
                <td> <input type='text' name='away_pens' placeholder='Penalty Kicks'/></td>
            </tr> 
            <tr>
                <td> <input type='text' name='home_free' placeholder='Free Kicks'/></td>
                <td> <input type='text' name='away_free' placeholder='Free Kicks'/></td>
            </tr>
            <tr>
                <td> <input type='text' name='home_p_total' placeholder='Total Passes'/></td>
                <td> <input type='text' name='away_p_total' placeholder='Total Passes'/></td>
            </tr>
            <tr>
                <td> <input type='text' name='home_p_complete' placeholder='Complete Passes'/></td>
                <td> <input type='text' name='away_p_complete' placeholder='Complete Passes'/></td>
            </tr>

        </table>

        <select name='access'>
                <option value='public'>Public</option>
                <option value='private'>Private</option>
        </select>

        <input type='submit' name='submit' value='Save Prediction'/>
        </form>
    </body>
    </html>
    ";


    if (isset($_POST['submit'])){
        $home_goals = $_POST['home_goals'];
        $away_goals = $_POST['away_goals'];
        $home_possession = $_POST['home_possession'];
        $away_possession = $_POST['away_possession'];
        $home_shots = $_POST['home_shots'];
        $away_shots = $_POST['away_shots'];
        $home_target = $_POST['home_target'];
        $away_target = $_POST['away_target'];
        $home_yellow = $_POST['home_yellow'];
        $away_yellow = $_POST['away_yellow'];
        $home_red = $_POST['home_red'];
        $away_red = $_POST['away_red'];
        $home_subs = $_POST['home_subs'];
        $away_subs = $_POST['away_subs'];
        $home_corners = $_POST['home_corners'];
        $away_corners = $_POST['away_corners'];
        $home_pens = $_POST['home_pens'];
        $away_pens = $_POST['away_pens'];
        $home_free = $_POST['home_free'];
        $away_free = $_POST['away_free'];
        $h_pass_total = $_POST['home_p_total'];
        $a_pass_total = $_POST['away_p_total'];
        $h_pass_complete = $_POST['home_p_complete'];
        $a_pass_complete = $_POST['away_p_complete'];
        $visibility =$_POST['access'];
        $home_team = $_POST['home_team'];
        $away_team = $_POST['away_team'];
        $name = $_POST['prediction_name'];
        $id;
        $game_id;
        $location;
        $status;
        $round_number;
        $stats_id = 
        $winnner = 0;
        if($home_goals > $away_goals){
            $winner = $home_team;
        }else if ($home_goals < $away_goals){
            $winner = $away_team;
        }else{
            $winner = -1;
        }


        $get_row_sql = "select * from game_predictions";
        $get_row_query = mysqli_query($conn, $get_row_sql);
        if(!$get_row_query){
            echo $conn->error;
        }else{
            $id = mysqli_num_rows(get_row_query)+1;
        }


        $game_sql = "select * from games where hometeam_id = '$home_team' and awayteam_id = '$away_team' and status = 'not_played'";
        $game_query = mysqli_query($conn, $game_sql);
        if(!$game_query){
            echo $conn->error;
        }else{
            if(mysqli_num_rows($game_query) != 0){
                $current_game = mysqli_fetch_assoc($game_query);
                $game_id = $current_game['gameid'];
                $location = $current_game['location'];
                $stats_id = $current_game['stats_id'];
                $round_number = $current_game['round_number'];

            }
        }

        $username = "5";
        $type = "league";

        $game_prediction_sql = "insert into game_predictions(game_prediction_id, gameid, hometeam_id, awayteam_id, stats_predictions_id, visibility,userid, name, location, status, round_number, winnner)";
        $game_prediction_sql."values ('$id','$game_id','$home_team','$away_team','$stats_id','$visibility','$username','$name','$location', '$status','$round_number')"
        $game_prediction_query = mysqli_query($conn, $game_prediction_sql);

        $prediction_stats_sql = "insert into stats_predictions(statsid, gameid, type, home_team_id, away_team_id, home_possession, away_possession, home_shots, away_shots, home_shots_on_target, away_shots_on_target, home_yellow_cards, away_yellow_cards, home_red_cards, away_red_cards, home_subs, away_subs, home_corners, away_corners, home_goals, away_goals, home_pens, away_pens, home_freekicks, away_freekicks, home_pass_total, away_pass_total, home_complete_passes, away_complete_passes, visibility)";
        $prediction_stats_sql."values('$stats_id','$game_id','$type','$home_team','$away_team','$home_possession','$away_possession','$home_shots','$away_shots','$home_target','$away_target','$home_yellow','$away_yellow','$home_red','$away_red','$home_subs','$away_subs','$home_corners', '$away_corners','$home_goals','$away_goals','$home_pens','$away_pens','$home_free','$away_free','$h_pass_total','$a_pass_total','$h_pass_complete','$a_pass_complete','$visibility')";
        $prediction_query = mysqli_query($conn, $prediction_stats_sql);

        if(!$prediction_query){
            echo $conn->error;
        }else{
            header("Location:view_predictions.php");
        }

    }


?>
