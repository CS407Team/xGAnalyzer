<?php
require_once "connect.php";

if(isset($_POST['username']) && isset($_POST['password'])) {
    $username = validate_username($_POST['username']);
    $password = validate_password($_POST['password']);
    $userType = '';
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
        header("Location:userpage.php");
    } else {
        header("Location:userpage.php");
    }
}

$_SESSION["username"] = $username;
$_SESSION["password"] = $password;

function validate_username($data){
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
}