// Insert database
<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "myDB";

$connection = new mysqli($servername, $username, $password);
// Connect to MySQL server
if(!$connection->connect_error) {
    die('Not connectedL' . $connection->connect_error);
}
echo "Connected successfully";

$sql = "INSERT INTO `markers` (`id`, `name`, `address`, `lat`, `lng`, `type`) VALUES ('1', 'Love.Fish', '580 Darling Street, Rozelle, NSW', '-33.861034', '151.171936', 'restaurant')";

if($connection->query($sql) ===  TRUE) {
    echo "New record created successfully";
} else {
    echo "Error: " . $sql . "<br>" . $connection->error;
}

$connection->close();
?>
