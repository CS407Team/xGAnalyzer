<?php
    include("connect.php");
    
    $sql = "select * from teams";
    $query = mysqli_query($conn, $sql);

    

    echo "
        <form method='POST' action='get_teams.php'>
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
        </form>
    ";


?>
