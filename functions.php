<?php

function getTaskNumber($taskName) {
    switch ($taskName) {
        case("reuqested_articles"):
            return 1;
            break;
        case("TEMPLATE"):
            return 0;
            break;
        default:
            return 999;
            break;
    }
}

function checkRun($task, $runUrl) {

    @$global = file_get_contents($runUrl . "&action=raw");
    @$local = file_get_contents("{$runUrl}/{$this->getTaskNumber($task)}&action=raw");

    if ($global == "on" && $local == "on") {
        return true;
    }
    else {
        return false;
    }
}

function insertRequest($pageString = "", $reqNum = "unknown", $title = "", $description="", $sources = "", $user = "") {
    $template = "{{User:Matthewrbot/Requests}}";

    // Processing script, to build a string template

    $reqString = "* {{Article request |title = {$title} |description = {$description} |user={$user} |sources={$sources} |date=~~~~~}} <!-- Request #{$reqNum} -->";

    if ( strpos($pageString, $template) ) {
        $return = str_replace($template,$template . "\r" . $reqString, $pageString);
    }
    else {
        $return = str_replace("[[Category:Requested Articles Pages with no template]]", "", $pageString);
        $return .= $reqString;
        $return .= "\r\r[[Category:Requested Articles Pages with no template]]";
    }

    $return = str_replace("\r\r*", "\r{{", $return);
    $return = str_replace("\n\n*", "\r*", $return);

    return $return;
}