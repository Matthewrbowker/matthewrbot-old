<?php
require('includes.php');

if (!isset($argv[1])) die("No task defined!\r\n");

$task = $argv[1];

ini_set('user_agent', 
  "Matthewrbot - [[:w:en:User:Matthewrbowker]] - {$version} - Task {$task}");
date_default_timezone_set("UTC");

if (!checkRun($task, $controlUrl)) die("Configuration set to off... exiting.\n\n");

$x = Peachy::newWiki("Matthewrbot" ); //Loads the config file
$db = new wpDatabase($dbhost, $dbname, $dbuser, $dbpw);

if (class_exists($task)) {
    $mod = new $task($db, $x);
} else {
    die("Error including module\r\n");
}

$return = $mod->execute();

if ($return) {
    print "Module completed successfully\r\n\r\n";
    return 0;
}
else {
    print "Module did not complete successfully\r\n\r\n";
    return 1;
}