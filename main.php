<?php
require('includes.php');

if (!isset($argv[1])) die("No task defined!\r\n");

$task = $argv[1];

ini_set('user_agent', 
  "Matthewrbot - [[:w:en:User:Matthewrbowker]] - {$version} - Task {$argv[1]}");
date_default_timezone_set("UTC");

if (!checkRun($task, $controlUrl)) die("Configuration set to off... exiting.\n\n");

$x = Peachy::newWiki("Matthewrbot_local"); //Loads the config file
$db = new wpDatabase($dbhost, $dbname, $dbuser, $dbpw);

$mod = new $task($db, $x);

$return = $mod->execute();

if ($return) {
    return 0;
}
else {
    return 1;
}