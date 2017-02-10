package Includes;

import java.net.Socket;

import java.io.PrintWriter;
import java.io.InputStreamReader;
import java.io.BufferedReader;

public class ircd {
    private config con;
    private logging log;
    private queuep q;
    private Socket socket;
    private PrintWriter out;
    private BufferedReader in;
    private BufferedReader stdIn;
    private String server = "chat.freenode.net";
    private int port = 6667;
    private String nicks[];
    private String password = "8zsexw9XADut=C+eXEk6MyquUYJebb";
    private String chans[];
    private int chansCount = 0;
    private char trigger = '?';
    private String nick;
    private int tick;

    private void ircDo(String action) {
        this.ircDo(action, "", "");
    }

    private void ircDo(String action, String channel) {
        this.ircDo(action, channel, "");
    }

    private void ircDo(String action, String channel, String other) {
        action = action.replace("\n", "");
        channel = channel.replace("\n", "");
        other = other.replace("\n", "");
        String string = action;
        if (channel != "") { string += " " + channel; }
        if (other != "") {string += " :" + other; }
        string += "\r\n";
        out.println(string);
        System.out.print("\tSENDING: " + string);
    }
    private boolean canDo(String hostmask) {
        System.out.println(hostmask);
        return hostmask.equals("wikimedia/matthewrbowker");
    }
    private void say(String channel, String message) {
        this.ircDo("PRIVMSG", channel, message);
    }
    private void rejoin(String channel) {
        this.ircDo("PART", channel, "Rejoining per request");
        this.ircDo("JOIN", channel);
    }
    private void rejoinAll() {
        for (String row : chans) {
            this.rejoin(row);
        }
    }
    private boolean isInChannel(String channel) {
        for (int i = 0; i < chansCount; i++) {
            if (chans[i].equals(channel)) {
                return true;
            }
        }

        return false;
    }

    public void registerChannel(String channelName) {
        this.chans[this.chansCount] = channelName;
        this.chansCount ++;
    }

    public ircd(config tempCon, logging tempLog, queuep tempQueue) throws Throwable {
        this.con = tempCon;
        this.log = tempLog;
        this.q = tempQueue;

        this.nicks =  new String[10];
        this.nicks[0] = "Matthewrbot";
        this.nicks[1] = "Matthewrbot_";

        this.chans = new String[100];

                this.socket = new Socket(server, port);
        this.out =
                new PrintWriter(this.socket.getOutputStream(), true);
        this.in =
                new BufferedReader(
                        new InputStreamReader(this.socket.getInputStream()));
        this.stdIn =
                new BufferedReader(
                        new InputStreamReader(System.in));
    }

    public void run() throws Throwable{
        Thread.sleep(5);
        this.nick = this.nicks[0];
        this.ircDo("USER", " " + this.nick + " " + this.nick + " " + this.nick + " " + this.nick + " " + this.nick );
        this.ircDo("NICK", this.nick);
        this.say("NickServ", "IDENTIFY " + this.nick + " " + this.password);
        Thread.sleep(5);

        for(int i = 0; i < chansCount; i++) {
            this.ircDo("JOIN", chans[i]);
        }

        String data;
        String allData[];
        String firstWord;
        String message;
        String holdValue[];

        String sendNick;
        String sendCloak;

        boolean ready = false;

        allData = new String[100];

        while(true) {
            if((in.ready())) {
                data = in.readLine();
                log.string(data);
                allData = data.split(" ");

                if(allData[0].equals("PING")) {
                    this.ircDo("PONG ", "", allData[1].substring(1));
                }
                else if (allData[0].matches(".*!.*@.*")) {
                    if (allData[1].equals("JOIN")) {
                        if (allData[2].equals(chans[0])) {
                            // We've joined our first channel - we can now be ready.
                            ready = true;
                        }
                    }
                    else if (allData[1].equals("KICK")) {
                        if (allData[3].equals(nick)) {
                            log.string("I've been kicked out of " + allData[2]);
                        }
                    }
                    else if (allData[1].equals("PRIVMSG")) {
                        sendNick = allData[0].split("!")[0];
                        sendCloak = allData[0].split("@")[1];
                        message = data.split(":")[2];
                        if (message.indexOf(' ') > -1) { message = message.substring(message.indexOf(" ")); }
                        firstWord = allData[3].substring(1);
                        if (firstWord.equals(this.trigger + "say")) {
                            this.say(allData[2], message);
                        }
                        else if (firstWord.equals(this.trigger + "about")) {
                            this.say(allData[2], sendNick + ": I am Matthewrbot, written by Matthew Bowker.  I am currently running version 0.1devel1, under Java version " + System.getProperty("java.version") + ".  My source code is at <https://github.com/matthewrbowker/matthewrbot>.");
                        }
                        else if (firstWord.equals(this.trigger + "ping")) {
                            this.say(allData[2], "pong");
                        }
                        else if (firstWord.equals(this.trigger + "join")) {
                            if (!this.canDo(sendCloak)) {
                                this.say(allData[2], "You are not allowed to give me that command");
                                continue;
                            }
                            this.chans[this.chansCount + 1] = message;
                            this.chansCount++;
                            this.ircDo("JOIN", message);
                        }
                        else if (firstWord.equals(this.trigger + "rejoin")) {
                            if (!this.canDo(sendCloak)) {
                                this.say(allData[2], "You are not allowed to give me that command");
                                continue;
                            }
                            this.rejoin(allData[2]);
                        }
                        else if (firstWord.equals(this.trigger + "quit")) {
                            if (!this.canDo(sendCloak)) {
                                this.say(allData[2], "You are not allowed to give me that command");
                                continue;
                            }
                            break;
                        }
                    }
                }
            }
            else {
                if ((this.tick % 1000000) == 0 && ready) {
                    if (q.hasItems()) {
                        holdValue = q.get();

                        if (!this.isInChannel(holdValue[0])) {
                            // We're not joined to that channel..
                            ircDo("JOIN", holdValue[0]);
                            this.say(holdValue[0], holdValue[1]);
                            ircDo("PART", holdValue[0]);
                        }
                        else {
                            this.say(holdValue[0], holdValue[1]);
                        }
                    }
                    tick = 0;
                }
            }

            tick++;

        }
    this.ircDo("QUIT", "", "SHUTDOWN: Requested by operator.");
    Thread.sleep(1000);
    }
}
