<?php
include("connect.php");


echo"

<form method='POST' action='get_fixtures.php'>
	<select name='game_id'>

";

$sql = "select * from games";
$query = mysqli_query($conn,$sql);
if($query){
while($game = mysqli_fetch_assoc($query)){
        $home_id = $game['hometeam_id'];
        $away_id = $game['awayteam_id'];
        $stats_id = $game['stats_id'];
        $winning_id = $game['winner_id'];
	$winning_team = "";
	$game_id = $game['gameid'];

        if($stats_id){
                $home_sql = "select * from teams where team_id='$home_id'";
                $away_sql = "select * from teams where team_id='$away_id'";

                $home_query = mysqli_query($conn, $home_sql);

                $home = "";
                $away = "";
                if($home_query){
                        while($current_home = mysqli_fetch_assoc($home_query)){
                                $home = $current_home['team_name'];
                        }
                }else{
                        echo $conn->error;
                }


                $away_query = mysqli_query($conn, $away_sql);
                if($away_query){
                        while($current_away = mysqli_fetch_assoc($away_query)){
                                $away = $current_away['team_name'];
                        }
                }else{
                        echo $conn->error;
                }

		echo "<option value=$game_id>".$home ." vs ". $away."</option>";
        }
    }
}


echo "</select>

	<input type='submit' name='submit' value='View Prediction'/>
	</form>
";

?>
