<?php
require_once "connect.php";

if(isset($_POST['username']) && isset($_POST['password'])) {
    $username = $_POST['username'];
    $password = $_POST['password'];
}


if(empty($username)) {
    echo 'Username required';
}
if(empty($password)) {
    echo 'Password required';
}
session_start();
$sql = "SELECT * FROM users WHERE username = '$username' AND password= '$password'";
$dataentry = $conn->query ($sql);

if(mysqli_num_rows($dataentry) === 1) {
    $row = mysqli_fetch_assoc($dataentry);
    if($row['username'] === $username && $row['password'] === $password) {
        header("Location: http://34.125.181.75/phpAnalyzer/userpage.php?username=$username?league=1");
    } 
}
else {
	header("Location: http://34.125.181.75/phpAnalyzer/usernotfound.php");
}

$_SESSION["username"] = $username;
$_SESSION["password"] = $password;
echo 'login';
//header("Location: http://34.125.181.75/phpAnalyzer/userpage.php");

/*function validate_username($data){
    if (preg_match('/^[a-zA-Z0-9]+$/', $data) == 0) {
        exit('Username cannot contain special characters!');
    }
    return($data);
}
function validate_password($data){
    if (preg_match('/^[a-zA-Z0-9]+$/', $data) == 0) {
        exit('Enter Valid Password');
    }
    return($data);
}*/
