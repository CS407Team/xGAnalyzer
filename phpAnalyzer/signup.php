<?php
require_once "connect.php";

if(isset($_POST['susername']) && isset($_POST['spassword'])) {
    $susername = $_POST['susername'];
    $spassword = $_POST['spassword'];
    $sfirstname = $_POST['sfirstname'];
    $slastname = $_POST['slastname'];
    $semail = $_POST['semail'];
}


if(empty($username)) {
    echo 'Picking Username required';
}
if(empty($password)) {
    echo 'Picking Password required';
}
session_start();
$sql2 = "INSERT INTO  users VALUES(6,'".$susername."','".$sfirstname."','".$slastname."','".$semail."','"
.$spassword."')";
$conn->query($sql2);

header("Location:index.php");

$_SESSION["susername"] = $susername;
$_SESSION["spassword"] = $spassword;

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
