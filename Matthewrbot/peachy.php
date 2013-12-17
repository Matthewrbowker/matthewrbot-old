<?php

require('includes.php');

date_default_timezone_set("UTC");

$x = Peachy::newWiki("Matthewrbot"); //Loads the config file

// $sites = new SiteMatrix( $x ); //Generates sitematrix, logic in Plugins/sitematrix.php

$page = initPage( "User:Matthewrbot/testbed1");
if ($page != null && $page->get_text() != NULL) {
	echo $page->get_text();
}
else {
	echo "NULL";
}

sleep(0.5);

echo "\n\n";

//$page->edit(insertRequest($page -> get_text(), "Testing", "This is a test edit, please ignore", "http://www.example.com", "Matthewrbowker"), "Inserting request for [[Testing]]");
