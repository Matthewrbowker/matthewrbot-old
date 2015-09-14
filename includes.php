<?php

require("config.php");

// Local configuration file, define the variables here.
require("config.inc.php");

require("wpDatabase.php");

require('functions.php');

require("Peachy/Init.php");

foreach(glob('modules/*.php') as $file) {
    require $file;
}