<?php
require('includes.php');

if (!isset($argv[1])) die("Died!\r\n");
getRequestedFile($modMap, $argv[1] - 1);

ini_set('user_agent', 
  "Matthewrbot - [[:w:en:User:Matthewrbowker]] - {$version} - Task {$argv[1]}");
date_default_timezone_set("UTC");

if (!checkRun($argv[1], $controlUrl)) die("Configuration set to off... exiting.\n\n");

$x = Peachy::newWiki("Matthewrbot_local"); //Loads the config file
$db = new wpDatabase($dbhost, $dbname, $dbuser, $dbpw);

$mod = new module($db, $x);

$return = $mod->execute();

if ($return) {
	return 0;
}
else {
	return 1;
}