<?php
    include("connect.php");
    
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

        <form method='POST' action='get_teams.php'>
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


?>
