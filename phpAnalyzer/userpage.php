<html>
<head>
    <style>
        .container0 {
          width: calc((100% - 130px)/5.5*2.35);
          padding: 0px 20px;
          height: 100px;
          background-color: #80e6e6;
          border: 1px solid black;
          float: left;
          display: block;
          font-size: xx-large;
        }
        .container1 {
          width: calc((100% - 130px)/5.5);
          padding: 0px 20px;
          height: 100px;
          background-color: #b746eb;
          border: 1px solid black;
          float: left;
          display: block;
          font-size: medium;
        }
        .container2 {
          width: calc((100% - 130px)/5.5);
          padding: 0px 20px;
          height: 100px;
          background-color: #e33bcd;
          border: 1px solid black;
          float: left;
          display: block;
          font-size: medium;
        }
        .container3 {
          width: calc((100% - 130px)/5.75);
          padding: 0px 20px;
          height: 100px;
          background-color: #f0279f;
          border: 1px solid black;
          float: left;
          display: block;
          font-size: medium;
        }
        .container5 {
            padding-top: 25px;
            background-color: #0096FF;
            color: #0096FF;
            height: 700px;
            font-size: xx-large;
        }
        .container6 {
            margin-left: 100px;
            margin-right: 80px;
            padding-top: 25px;
            position: relative;
            background-color: lightblue;
            height: 600px;
            font-size: xx-large;
        }
        h1 {
        	position: relative;
        	color: grey;
        }
        h2 {
            font-size: medium;
            color: lightgray;
        }
        .header{
            padding-left: 100px;
        }
        .header img {
            float: left;
            width: 250px;
            height: 150px;
        }
        Body {
            font-family: Calibri, Helvetica, sans-serif;
            background-color: darkblue;
        }
	form {
           font-size:large;
	}
    </style>
</head>
<body>
    <div class="header">
    <img src="https://i.ibb.co/K7K5D49/xgGraph.png" alt="logo" />
    <h1>&ensp;xG Analyzer</h1>
    </div>
      <h2>&emsp; We analyze, you decide </h2>
    <br><br><br>
    <div class="container">
  	<?php 
	$url = $_SERVER['REQUEST_URI']; 
        $temp = $url;
        $arr = explode("=",$temp);
        $username = $arr[1];
	echo '<div class="container0">';
        echo '<br>';
        echo '&emsp;&emsp;Welcome back '.$username.'!'.'</div>'; ?>
        <div class="container1"><br><br><a href='match_prediction.php'>Predict a  match based on xG graph</a><br/>
	<a href='search_predictions.php'>Search for player performance ratings</a></div>
        <div class="container2"><br><br>Find game result based on xG graph</div>
        <div class="container3"><br><br>Generate xG graph for soccer match</div>
    </div>
    <br/><br/><br/><br/><br/><br/><br/>
    <div>
        <div class="container5">
            <div class="container6">
                <br>
                    <?php 
echo '&emsp;&emsp;Pick your favourite league: <br>';
                    echo '&emsp;&emsp;Leagues List :'; ?>  
                   <?php
    include("connect.php");
    $url1 = $_SERVER['REQUEST_URI']; 
    $temp1 = $url1;
    $arr1 = explode("=",$temp1);
    $arr11 = explode("?",$arr1[1]);
    $username = $arr11[0];
    $sql1 = "select * from tournaments";
    $query1 = mysqli_query($conn, $sql1);
    $tour = 1;
    if(isset($_POST['league'])){
        $tour = $_POST['league'];
    }
    //include_once('../userpage.php?username='.$username.'?league='.$tour);
    echo "
        <form method='POST' name='league' action='userpage.php?username=$username?league=$tour'>
           &emsp;&emsp;&emsp;&emsp;<select name='league'>";
            if(!$query1){
                echo $conn->error;
            }else{
                while($league = $query1->fetch_assoc()){ 
                    $league_id = $league['tournament_id'];
                    $league_name = $league['name'];
                    echo "<option value='$league_id'>$league_name</option>";
                }
            }
            echo "</select><br>&emsp;&emsp;&emsp;&emsp;<button action='addteams.php' type='submit'>Select League</button></form>"
?>
                    <?php 
                    echo '<br><br>';
                    echo '&emsp;&emsp;Pick your favourite teams: <br>';
                    echo '&emsp;&emsp;Teams List :'; ?>  
                   <?php
    include("connect.php");
    $url2 = $_SERVER['REQUEST_URI']; 
    $arr2 = explode("=",$url);
    $arr22 = explode("?",$arr2[1]);
    $username = $arr22[0];
    $l_id = substr($arr2[2],0,1);
    echo 'l_id is'.$l_id;
    $sql = "select * from teams where tournament_id=".$l_id;
    $query = mysqli_query($conn, $sql);
    echo "
        <form method='POST' action='get_teams.php'>
           &emsp;&emsp;&emsp;&emsp;<select name='home_team'>";
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
            echo "</select>";
            echo "<br>";
            echo "&emsp;&emsp;&emsp;&emsp;<button action='addteams.php' type='submit'>Add Teams</button></form>";
?>
            </div>
        </div>
    </div>
</body>
</html>

