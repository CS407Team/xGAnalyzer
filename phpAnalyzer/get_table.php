<?php
include("connect.php");

if(isset($_POST['submit'])){


$round = $_POST['round'];

$sql = "select * from season_table where round_number = '$round'";
$query = mysqli_query($conn,$sql);

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

<h2>Week ".$round." Table Prediction</h2>";
      echo"<table> 

        <tr><th>#</th><th>Team</th><th>P</th><th>W</th><th>D</th><th>L</th><th>Pts</th></tr>";


if($query){
	$team_id="";
	$tournament_id="";
	$team_position="";
	$team_points="";
	$games_played="";
	$won="";
	$lost="";
	$drawn ="";
	$round_number  ="";
	$team = "";

	while($current_standing = mysqli_fetch_assoc($query)){

		$team_id= $current_standing['team_id'];
		$tournament_id= $current_standing['tournament_id'];
		$team_position= $current_standing['team_position'];
		$team_points= $current_standing['team_points'];
		$games_played= $current_standing['games_played'];
		$won= $current_standing['won'];
		$lost= $current_standing['lost'];
		$drawn = $current_standing['drawn'];
		$round_number = $current_standing['round_number'];

		$team_sql = "select * from teams where team_id='$team_id'";

                $home_query = mysqli_query($conn, $team_sql);

                $home = "";
                if($home_query){
                        while($current_home = mysqli_fetch_assoc($home_query)){
                                $team = $current_home['team_name'];

                        }
                }else{
                        echo $conn->error;
                }

		echo "<tr><td>".$team_position."</td><td>".$team."</td><td>".$games_played."</td><td>".$won."</td><td>".$drawn."</td><td>".$lost."</td><td>".$team_points."</td></tr>";



	}

}else{
	echo $conn->error;
}

echo "</table></body></html>";
}
?>
