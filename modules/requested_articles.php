<?php

class module {
    private $db;
    private $p;
    function __construct(wpDatabase $dbTemp, Wiki $pTemp) {
        $this->db = $dbTemp;
        $this->p = $pTemp;
    }

    private function insertRequest($pageString = "", $reqNum = "unknown", $title = "", $description="", $sources = "", $user = "") {
        $template = "{{User:Matthewrbot/Requests}}";

        // Processing script, to build a string template

        $reqString = "* {{Article request |title = {$title} |description = {$description} |user={$user} |sources={$sources} |date=~~~~~}} <!-- Request #AR-{$reqNum} -->";

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

    function execute() {
        // NEEDS TO BE EDITED
        $qResult = $this->db->selectQuery("*", "requests", ["done",'0'], 1000);

        foreach ($qResult as $row) {
            $page = initPage( "User:Matthewrbot/testbed1");

            if ($page != null && $page->get_text() != NULL) {
                //echo $page->get_text();:
            }
            else {
                echo "NULL";
            }

            $id = $row['id'];

            $newPageText = $this->insertRequest($page -> get_text(), $row['id'], $row['subject'], $row["Description"], $row["Sources"], $row["Username"]);
            echo $newPageText;
            $page->edit($newPageText, "Inserting request for [[{$row['subject']}]]");

            $this->db->updateQuery("requests",['done','1'],['id',$id]);

            sleep('5');
            // END
        }
        return 1;
    }
}