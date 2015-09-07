<?php

class wpDatabase {
    private $p;

    function dbError($ex, $additional = "") {
        echo "Database Error: " . $ex->getMessage() . " - $additional\r\n";
        die();
    }

    function __construct($dbHost,$dbName,$dbUser,$dbPass) {
        $pdoString = "mysql:host={$dbHost};dbname={$dbName};charset=utf8";


        try {
            $this->p = new PDO($pdoString, $dbUser, $dbPass);
        }
        catch(PDOException $ex) {
            $this->dbError($ex, $pdoString);
        }

    }

    private function query($query, ...$values) {
        print $query;
        print $values;
    }

    function selectQuery($fields, $table, $where = "1", $limit = NULL) {
        $this->query("SELECT * FROM `table` WHERE 1");
    }
}