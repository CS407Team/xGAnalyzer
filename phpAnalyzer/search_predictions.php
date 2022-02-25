<?php
include("connect.php");

if(isset($_POST['submit'])){

    $team = $_POST['team'];
    $name = strtolower($_POST['player_name']);
    $sql = "select * from player where teamid='$team'";
    $query = mysqli_query($conn, $sql);
    if(!$query){
        
    }else{
        while($player = mysqli_fetch_assoc($query)){
            $player_name = strtolower($player['playername']);
		if(strpos($player_name, $name) !== false){
//                echo "Found<br/>";
		echo "<p>Prediction for ".$player['playername']."</p><br/><br/>";
		$playerid = $player['playerid'];
                $get_predictions = "select * from player_performance_prediction where playerid='$playerid'";
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
                        $num_successful_tackles = $prediction['num_successful_tackles'];
                        $yellow = $prediction['yellow_cards'];
                        $red = $prediction['red_cards'];
                        $goals = $prediction['goals'];
                        $total_shots = $prediction['total_shots'];
                        $target = $prediction['shots_on_target'];
                        $total_passes = $prediction['total_passes'];
                        $complete_passses = $prediction['complete_passes'];
                        $total_saves = $prediction['total_saves'];
                        $goals_conceded = $prediction['goals_conceded'];
                        $total_crosses = $prediction['total_crosses'];
                        $assists = $prediction['assists'];
                        $visibility = $prediction['visibility'];
	        	echo "<tr><th>Goals</th><td>".$goals."</td>";
	        	echo "<tr><th>Total Tackles </th><td>".$num_tackles."</td>";
	        	echo "<tr><th>Successfull Tackles </th><td>".$num_successful_tackles."</td>";
	        	echo "<tr><th>Yellow Cards </th><td>".$num_tackles."</td>";
	        	echo "<tr><th>Red Cards </th><td>".$num_tackles."</td>";
	        	echo "<tr><th>Total Shots </th><td>".$total_shots."</td>";
	        	echo "<tr><th>Shots on Target </th><td>".$target."</td>";
	        	echo "<tr><th>Total Passes </th><td>".$total_passes."</td>";
	        	echo "<tr><th>Complete Passes </th><td>".$complete_passses."</td>";
	        	echo "<tr><th>Total Saves </th><td>".$total_saves."</td>";
	        	echo "<tr><th>Goals Conceded </th><td>".$goals_conceded."</td>";
	        	echo "<tr><th>Total Crosses </th><td>".$total_crosses."</td>";
	        	echo "<tr><th>Assists </th><td>".$assists."</td>";
	        	echo "<tr><th>Visibility </th><td>".$visibility."</td>";

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
    echo "
<br/><br/><br/>    <form method='POST' action='search_predictions.php'>
            <select name='team'>";

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

            <input name='player_name' type='text' placeholder='Player Name'/><br/>
            <input type='submit' name='submit' value='Search'/>
        </form>
    ";

?>
