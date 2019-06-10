<?php
    require_once "dbconfig.php";
    $conn = new PDO("mysql:host=localhost;dbname=EventMap", $user, $password);
    echo "Connected to EventMap at localhost successfully.";
    $sql = "SELECT * FROM `maps`";
    // $q = $conn->query($sql);
    $q = $conn->prepare($sql);
    $q->execute(array());
    $q->setFetchMode(PDO::FETCH_ASSOC);
?>