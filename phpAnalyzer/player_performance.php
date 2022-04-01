<?php
include("connect.php");

if(isset($_POST['submit'])){

    $team = $_POST['home_team'];
    $away = $_POST['away_team'];
    $name = strtolower($_POST['player_name']);
    $sql = "select * from player where teamid='$team'";
    $query = mysqli_query($conn, $sql);
    if(!$query){
       	echo $conn->error;
    }else{

        while($player = mysqli_fetch_assoc($query)){
            $player_name = strtolower($player['playername']);
                if(strpos($player_name, $name) !== false){
                echo "<h2>Prediction for ".$player['playername']."</h2><br/><br/>";
                $playerid = $player['playerid'];
                $get_predictions = "select * from player_performance where playerid='$playerid'";
                $prediction_query = mysqli_query($conn, $get_predictions);
                if(!$prediction_query){
                        echo $conn->error;
                }else{

        echo "
    <!DOCTYPE html>
    <html>
    <style>
    table, th, td {
    border:1px solid black;
    }
    </style>
    <body><table>";
                    while($prediction = mysqli_fetch_assoc($prediction_query)){
			$num_tackles = $prediction['num_tackles'];
                        $yellow = $prediction['yellow_cards'];
                        $red = $prediction['red_cards'];
                        $goals = $prediction['goals'];
                        $total_shots = $prediction['total_shots'];
                        $target = $prediction['shots_on_target'];
                        $total_passes = $prediction['total_passes'];
                        $complete_passses = $prediction['complete_passes'];
                        $total_saves = $prediction['saves'];
                        $goals_conceded = $prediction['goals_conceded'];
                        $assists = $prediction['assists'];
                        echo "<tr><th>Goals</th><td>".$goals."</td>";
                        echo "<tr><th>Total Tackles </th><td>".$num_tackles."</td>";
                        echo "<tr><th>Yellow Cards </th><td>".$num_tackles."</td>";
                        echo "<tr><th>Red Cards </th><td>".$num_tackles."</td>";
                        echo "<tr><th>Total Shots </th><td>".$total_shots."</td>";
                        echo "<tr><th>Shots on Target </th><td>".$target."</td>";
                        echo "<tr><th>Total Passes </th><td>".$total_passes."</td>";
                        echo "<tr><th>Complete Passes </th><td>".$complete_passses."</td>";
                        echo "<tr><th>Total Saves </th><td>".$total_saves."</td>";
                        echo "<tr><th>Goals Conceded </th><td>".$goals_conceded."</td>";
                        echo "<tr><th>Assists </th><td>".$assists."</td>";

                        }
                }
        echo"</table>";
                break;
            }else{
        }
        }
    }

}

echo "</body></html>";

$sql = "select * from teams";
    $query = mysqli_query($conn, $sql);
    $teams = array();
    echo "
<br/><br/><br/>    <form method='POST' action='player_performance.php'>
            <select name='home_team'>";

            if(!$query){
                echo $conn->error;
            }else{
                while($team = $query->fetch_assoc()){ 
		    array_push($teams,$team);
                    $id = $team['team_id'];
                    $tournament_id = $team['tournament_id'];
                    $name = $team['team_name'];
                    echo "<option value='$id'>$name</option>";
                }
            }
echo"
            </select>
	vs
	<select name='away_team'>
	<option value = '1'>Manchester City</option>
	<option value = '2'>Liverpool</option>
	<option value = '3'>Chelsea</option>
	<option value = '4'>West Ham</option>
	<option value = '5'>Manchester United</option>
	<option value = '6'>Arsenal</option>
	<option value = '7'>Wolves</option>
	<option value = '8'>Tottenham</option>
	<option value = '9'>Brighton</option>
	<option value = '10'>Southampton</option>
	<option value = '11'>Leicester</option>
	<option value = '12'>Aston Villa</option>
	<option value = '13'>Crystal Palace</option>
	<option value = '14'>Brentford</option>
	<option value = '15'>Leeds</option>
	<option value = '16'>Everton</option>
	<option value = '17'>Newcastle</option>
	<option value = '18'>Norwich</option>
	<option value = '19'>Watford</option>
	<option value = '20'>Burnley</option>

	</select>


            <input name='player_name' type='text' placeholder='Player Name'/><br/>
            <input type='submit' name='submit' value='Search'/>
        </form>
    ";

?>
