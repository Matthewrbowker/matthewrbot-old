<?php

class TEMPLATE {
    var $db;
    var $p;
    function __construct(wpDatabase $dbTemp, Wiki $pTemp) {
        $this->db = $dbTemp;
        $this->p = $pTemp;
    }

    function execute() {
        echo "We would execute our module here";
        return true;
    }
}