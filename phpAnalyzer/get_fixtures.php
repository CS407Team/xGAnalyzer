<?php
include("connect.php");

if(isset($_POST['submit'])){

$game = $_POST['game_id'];
$sql = "select * from games where gameid = '$game'";
$query = mysqli_query($conn,$sql);
if($query){
while($game = mysqli_fetch_assoc($query)){
	$home_id = $game['hometeam_id'];
	$away_id = $game['awayteam_id'];
	$stats_id = $game['stats_id'];
	$winning_id = $game['winner_id'];
	$winning_team = "";

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

if($winning_id == $home_id){
	$winning_team = $home;
}else if($winning_id == $away_id){
	$winning_team = $away;
}else{
	$winning_team = "None, its a draw/tie";
}


		$stats_sql = "select * from stats where statsid = '$stats_id'";
		$stats_query = mysqli_query($conn, $stats_sql);

		$round;
		$type;
		$home_team_id;
		$away_team_id;
		$away_possession;
		$home_possession;
		$away_shots;
		$home_shots;
		$home_shots_on_target;
		$away_shots_on_target;
		$home_yellow_cards;
		$away_yellow_cards;
		$home_red_cards;
		$away_red_cards;
		$home_goals;
		$away_goals;
		$home_pens;
		$away_pens;
		$home_freekicks;
		$away_freekicks;
		$home_pass_total;
		$away_pass_total;
		$home_complete_passes;
		$away_complete_passes;

		if($stats_query){
			while($stats=mysqli_fetch_assoc($stats_query)){
				$round                =  $stats['round'];
				$type                 =  $stats['type'];
				$home_team_id         =  $stats['home_team_id'];
 				$away_team_id         =  $stats['away_team_id'];
 				$away_possession      =  $stats['away_possession'];
				$home_possession      =  $stats['home_possession'];
				$away_shots           =  $stats['away_shots'];
 				$home_shots           =  $stats['home_shots'];
				$home_shots_on_target =  $stats['home_shots_on_target'];
 				$away_shots_on_target =  $stats['away_shots_on_target'];
 				$home_yellow_cards    =  $stats['home_yellow_cards'];
 				$away_yellow_cards    =  $stats['away_yellow_cards'];
				$home_red_cards       =  $stats['home_red_cards'];
 				$away_red_cards       =  $stats['away_red_cards'];
				$home_goals           =  $stats['home_goals'];
 				$away_goals           =  $stats['away_goals'];
 				$home_pens            =  $stats['home_pens'];
 				$away_pens            =  $stats['away_pens'];
				$home_freekicks       =  $stats['home_freekicks'];
 				$away_freekicks       =  $stats['away_freekicks'];
 				$home_pass_total      =  $stats['home_pass_total'];
 				$away_pass_total      =  $stats['away_pass_total'];
 				$home_complete_passes =  $stats['home_complete_passes'];
 				$away_complete_passes =  $stats['away_complete_passes'];


				if($home_possession > $away_possession){
					$away_possession = 100-$home_possession;
				} else if ($away_possession > $home_possession){
					$home_possession = 100-$away_possession;
				}
				/*

				if($home_possession > $away_possession){
					$away_possession = 100-$home_possesssion;
				}else if($away_possession > $home_possession){
					$home_possession = 100-$away_possession;
				}*/



echo "

<!DOCTYPE html>
<html>
<head>
<style>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #dddddd;
}
</style>
</head>
<body>

<h2>".$home." vs ".$away." Statistics Prediction</h2>"
;
      echo
	"<h3>Winner: ".$winning_team."</h3>
	 <table>

        <tr><th>Stat</th><th>Home Team</th><th>Away Team</th></tr>";
        echo "<tr><th>Team Name</th><td>".$home."</td><td>".$away."</td></tr>";
        echo "<tr><th>Possession</th><td>".$home_possession."</td><td>".$away_possession."</td></tr>";
        echo "<tr><th>Total Shots</th><td>".$home_shots."</td><td>".$away_shots."</td></tr>";
        echo "<tr><th>Shots on Target</th><td>".$home_shots_on_target."</td><td>".$away_shots_on_target."</td></tr>";
        echo "<tr><th>Yellow Cards</th><td>".$home_yellow_cards."</td><td>".$away_yellow_cards."</td></tr>";
        echo "<tr><th>Red Cards</th><td>".$home_red_cards."</td><td>".$away_red_cards."</td></tr>";
        echo "<tr><th>Penalties</th><td>".$home_pens."</td><td>".$away_pens."</td></tr>";
        echo "<tr><th>Free Kicks</th><td>".$home_freekicks."</td><td>".$away_freekicks."</td></tr>";
        echo "<tr><th>Total Passes</th><td>".$home_pass_total."</td><td>".$away_pass_total."</td></tr>";
        echo "<tr><th>Complete Passess</th><td>".$home_complete_passes."</td><td>".$away_complete_passes."</td></tr>";



			}
		}else{
			echo $conn->error;
		}


	}
}

}else{
	echo $conn->error;
}
}

echo "</table></body></html>";
?>

