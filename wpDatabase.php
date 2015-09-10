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

    private function query($query) {
        print "$query\r\n";
        try {
            $prepared = $this->p->prepare($query);
            $prepared->execute();
            return $prepared->fetchAll();
        }
        catch(PDOException $ex) {
            $this->dbError($ex, $query);
        }
    }

    function selectQuery($fields, $table, $where = "1", $limit = NULL) {
        $queryString = "SELECT ";
        $firstLoop = true;
        if (is_array($fields)) {
            foreach($fields as $value) {
                if (!$firstLoop) {$queryString .= ", ";}

                $queryString .= "`$value` ";
                $firstLoop = false;
            }
        } else {
            $queryString .= "$fields ";
        }

        $queryString .= "FROM `$table` ";

        if (is_array($where)) {
            $queryString .= "WHERE `$where[0]` = '$where[1]' ";
        } else {$queryString .= "WHERE $where";}

        if ($limit != NULL) {$queryString .= "LIMIT $limit"; }

        return $this->query($queryString);
    }

    function updateQuery($table, $field, $where) {
        $queryString = "UPDATE ";
        $queryString .= "`$table` ";
        $queryString .= "SET `$field[0]`='$field[1]' ";
        $queryString .= "WHERE `$where[0]` = '$where[1]'";
        return $this->query($queryString);
    }
}