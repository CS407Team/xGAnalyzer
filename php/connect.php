<?php
$servername = "localhost";
$username = "root";
$password = "V3z?RnzC";
// Create connection
$conn = new mysqli($servername, $username, $password,"analyzer");
// Check connection
if ($conn->connect_error) {``
  die("Connection failed: " . $conn->connect_error);
}
 echo "Connected successfully";
?>

