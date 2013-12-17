<?php

function checkRun() {
	

	$global = file_get_contents("https://en.wikipedia.org/wiki/User:Matthewrbot/Control?action=raw");
	$local = file_get_contents("https://en.wikipedia.org/wiki/User:Matthewrbot/Control/1?action=raw");

	if ($global == "on" && $local == "on") {
		return true;
	}
	else {
		return false;
	}
}

function insertRequest($pageString = "", $title = "", $description="", $sources = "", $user = "") {
	$template = "{{User:Matthewrbot/Requests}}";

	// Processing script, to build a string template

	$reqString = "* {{Article request |title = {$title} |description = {$description} |user={$user} |sources={$sources} |date=~~~~~}}";

	if ( strpos($pageString, $template) ) {
		$return = str_replace($template,$template . "\r" . $reqString, $pageString);
	}
	else {
		$return = str_replace(,$template . "\r" . $reqString, $pageString);;
	}

	return $return;
}