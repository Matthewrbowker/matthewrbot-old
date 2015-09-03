<?php
require('includes.php');

if (!isset($argv[1])) die("Died!\r\n");

date_default_timezone_set("UTC");

if (!checkRun($argv[1], $controlUrl)) die("Configuration set to off... exiting.\n\n");

$x = Peachy::newWiki("Matthewrbot_local"); //Loads the config file

$pdoString = "mysql:host={$dbhost};dbname={$dbname};charset=utf8";

try {
    $p = new PDO($pdoString, $dbuser, $dbpw);
}
catch(PDOException $ex) {
    echo "Problem connecting to the database: " . $ex->getMessage();
    die("\r");
}

$qResult = $p->query("SELECT * FROM `requests` where `done`='0'");

$values = $qResult->fetchAll();

foreach ($values as $row) {
    $page = initPage( "User:Matthewrbot/testbed1");

    if ($page != null && $page->get_text() != NULL) {
        //echo $page->get_text();
    }
    else {
        echo "NULL";
    }

    $id = $row['id'];

    $newPageText = insertRequest($page -> get_text(), $row['id'], $row['subject'], $row["Description"], $row["Sources"], $row["Username"]);
    echo $newPageText;
    $page->edit($newPageText, "Inserting request for [[{$row['subject']}]]");

    $update = $p -> prepare("UPDATE `requests` SET `done`='1' WHERE `id`='{$id}'");

    $update -> execute();

    sleep('5');
}

return 0;