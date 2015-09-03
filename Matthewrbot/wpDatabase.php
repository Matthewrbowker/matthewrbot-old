<?php

class wpDatabase {
	private $p;
	function __construct($dbHost,$dbName,$dbUser,$dbPass) {
		$pdoString = "mysql:host={$dbHost};dbname={$dbName};charset=utf8";


		try {
			$this->p = new PDO($pdoString, $dbUser, $dbPass);
		}
		catch(PDOException $ex) {
			echo "Problem connecting to the database: " . $ex->getMessage();
			die("\r");
		}

	}

	function query($query) {
		print $query;
	}
}