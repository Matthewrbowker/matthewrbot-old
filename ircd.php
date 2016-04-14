<?php

/*
This is an IRC Daemon.  It is started with nohup.  

It should query from a database, send the message, then remove the message from the database.
*/

// Prevent PHP from stopping the script after 30 sec
set_time_limit(0);

//error_reporting(0);

class ircd {
    private $q;
    private $socket;
    private $server = "chat.freenode.net";
    private $port = 6667;
    private $nicks = ["Matthewrbot", "Matthewrbot_"];
    private $password = "8zsexw9XADut=C+eXEk6MyquUYJebb";
    private $chans = ["##matthewrbot"];
    private $trigger = "?";
    private $nick;

    private function ircDo($action, $channel = "", $other = "") {
        $action = str_replace("\n", "", $action);
        $channel = str_replace("\n", "", $channel);
        $other = str_replace("\n", "", $other);
        $string = $action;
        if ($channel != "") { $string .= " $channel"; }
        if ($other != "") {$string .= " :$other"; }
        $string .= "\r\n";
        fputs($this->socket, $string);
        print $string;
    }

    private function canDo($hostmask) {
        print "$hostmask\n";
        return $hostmask == "wikimedia/matthewrbowker";
    }

    private function say($channel, $message) {
        $this->ircDo("PRIVMSG", $channel, $message);
    }


    private function rejoin($channel, $reqChanel) {
        $this->ircDo("PART", $channel, "Rejoining per request in $channel");
        $this->ircDo("JOIN", $channel);
    }

    private function rejoinAll($channel) {
        foreach ($this->chans as $row) {
            $this->rejoin($row, $channel);
        }
    }

    public function __construct() {
    }

    // public function __construct(queuep $q) {
    //    $this->q = $q;
    //}

    function run() {
        $this->nick = $this->nicks[0];
        $this->socket = fsockopen($this->server, $this->port) or die("Cannot connect");
        $this->ircDo("USER", "{$this->nick} {$this->nick} {$this->nick} {$this->nick} :{$this->nick}");
        $this->ircDo("NICK", $this->nick);
        $this->say("NickServ", "IDENTIFY {$this->nick} {$this->password}");
        sleep(5);
        $this->ircDo("JOIN", $this->chans[0]);

        while(1) {
            print "loop...\r\n";
            if($data = fgets($this->socket)) {

                print $data;
                $ex = explode(' ', $data);
                $rawcmd = explode(':', $ex[3]);
                @$oneword = explode('\n', $rawcmd);
                $channel = $ex[2];
                $nicka = explode('@', $ex[0]);
                $nickb = explode('!', $nicka[0]);
                $nickc = explode(':', $nickb[0]);

                @$host = $nicka[1];
                @$nick = $nickc[1];
                if($ex[0] == "PING"){
                    $this->ircDo("PONG ", "", substr($ex[1], 1));
                }

                $args = NULL; for ($i = 4; $i < count($ex); $i++) { $args .= $ex[$i] . ' '; }

                if ($rawcmd[1] == "{$this->trigger}about") {
                    $this->say($channel, "$nick: I am Matthewrbot, written by Matthew Bowker.  I am currently running version 0.1devel1.  My source code is at <https://github.com/matthewrbowker/matthewrbot>.");
                }
                elseif ($rawcmd[1] == "{$this->trigger}sayit") {
                    $this->say($channel, $args);
                }
                elseif ($rawcmd[1] ==  "{$this->trigger}md5") {
                    $this->say($channel, "MD5 " . MD5($args));
                }
                elseif ($rawcmd[1] == "{$this->trigger}ping") {
                    $this->say($channel, "PONG");
                }
                elseif ($rawcmd[1] == "{$this->trigger}join") {
                    $this->chans[] = $args;
                    $this->ircDo("JOIN", $args);
                }
                elseif ($rawcmd[1] == "{$this->trigger}rejoinall") {
                    if ($this->canDo($host)) {
                        $this->rejoinAll($channel);
                    }
                    else {
                        $this->say($channel, "{$nick}: You're not allowed to give me that command.");
                    }
                }
                elseif ($rawcmd[1] == "{$this->trigger}rejoin") {
                    if ($this->canDo($host)) {
                        $this->rejoin($args, $channel);
                    }
                    else {
                        $this->say($channel, "{$nick}: You're not allowed to give me that command.");
                    }
                }
                elseif ($rawcmd[1] == "{$this->trigger}quit") {
                    if ($this->canDo($host)) {
                        $this->ircDo("QUIT", "", "SHUTDOWN: Requested by operator.");
                        sleep(10);
                        return;
                    }
                    else {
                        $this->say($channel, "{$nick}: You're not allowed to give me that command.");
                    }
                }
            }
            else {
                print("\tNothing to do...\r\n");
            }
        }
    }
}

$irc = new ircd();

$irc->run();
