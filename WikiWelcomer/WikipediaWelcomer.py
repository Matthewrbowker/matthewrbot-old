#!/usr/bin/env python

import socket # Allows us to connect to the internet
import sys # System functions
import time # Time Functions
import threading # thread functions
import Queue
import WikiWelcomerModules
import urllib
import mwclient

urllib.urlretrieve('http://en.wikipedia.org/wiki/User:WikiWelcomer/Control?action=raw', 'status.wwbot')
f = open('status.wwbot')
status = f.read()
f.close()
if status == 'on':
    import socket # Allows us to connect to the internet
    import sys # System functions
    import time # Time Functions
    import Queue
    import urllib
    import mwclient
    import re

    global mainchan
    global botnick
    global version
    global irc
    global errorthrown

    mainchan = '##wikiwelcomertest';
    feedchan = '##wikipediawelcomer';
    botnick = 'WikiWelcomer';
    version = '5.1';

    network = 'irc.freenode.net' # Define as connection to Freenode
    port = 6667 # Define Port
    irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM ) # Initialize IRC
    irc.connect ( ( network, port ) ) # Connect
    irc.recv ( 4096 ) # Set Recieve port
    irc.send ( 'NICK ' + botnick + '\r\n' ) # /nick to Proper Username
    irc.send ( 'USER Welcomer Welcomer Welcomer :WikiWelcomer v.' + version + '\r\n' )  # Define user variables
    irc.send ( 'NS identify WikiWelcomer editor\r\n' ) # Identify
    time.sleep(6) # sleep for a bit so we don't join channels un-authed
    irc.send ( 'JOIN ' + mainchan + '\r\n' ); # Join channels
    irc.send ( 'JOIN ##matthewrbowker\r\n' );
    irc.send ( 'JOIN ##WikipediaWelcomer\r\n');
    check = 0;
    reset = Queue.Queue(1);
    fileupdate = Queue.Queue(1);
    updatemax = 10
    update = 0
else:
    print 'File is set to off, exiting'
    time.sleep(10)
    sys.exit()
    
def pingingout():
    updatemax = 10;
    update = 0;
    check = 0;
    checkmax = 300;
    checkmax=int(checkmax)
    reset.get()
    while True:
        time.sleep(1)
        print threading.enumerate()
        check=int(check)
        update=int(update)
        check = check+1
        update = update+1
        if check > checkmax:
            sys.exit()
        if reset.empty() == False:
            check = reset.get()
            check=int(check)

def datarecieve():
    while True:
        try:
            data = irc.recv ( 4096 )
            print data
#            if data.find( '[[' ):
#                link=findall('\[\[([^"]*)\]\]', data);
#                print link
            if data.find ( 'PING' ) != -1:
                reset.put('0');
                irc.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' ) # Send back data to server
            elif data.find ( 'gateway/web/freenode' ) != -1: # Check for IP Cloak
                user = data.split() [ 0 ] # Split down to just the user
                user = str(user) # Convert the variable to a string
                user = user.replace ( ':', '', 1) # Get rid of the colon at the beginning
                cloak = user.split( '@' ) [1]
                cloak = str(cloak)
                nick = user.split ( '!' ) [ 0 ] # Right, let's go down and remove the IP information
                nick = str(nick) # Convert the variable to a string
                if data.find ( 'JOIN ' + mainchan ) != -1: # Check to make sure they actually joined, instead of saying something
                    time.sleep(1) # Sleep for a second to make sure that they are up and can recieve
                    irc.send ( 'PRIVMSG ' + mainchan + ' :Hi, '+ nick + '!  Welcome to ' + mainchan + ', the help channel for the English Wikipedia.  Please type your question in the box below and wait for our helpers to respond. :) \r\n' );  # Welcome the user
                    irc.send ( 'PRIVMSG ##matthewrbowker :' + nick + ' ( ' + cloak + ' ) has joined ' + mainchan + '.\r\n' ); # Sends a message to the helpers channel
                    irc.send ( 'PRIVMSG ##WikipediaWelcomer :' + nick + ' ( ' + cloak + ' ) has joined ' + mainchan + '.\r\n' ); # Sends a message to the helpers channel
                    reset.put('0');
                elif data.find ( 'PART ' + mainchan ) != -1: # Check if the user parted
                    irc.send ( 'PRIVMSG ##matthewrbowker :' + nick + ' ( ' + cloak + ' ) has left ' + mainchan + '.\r\n' );
                    irc.send ( 'PRIVMSG ##WikipediaWelcomer :' + nick + ' ( ' + cloak + ' ) has left ' + mainchan + '.\r\n' );
                    reset.put('0');
                elif data.find ( ' QUIT :' ) != -1: #Check to see if the user quit
                    irc.send ( 'PRIVMSG ##matthewrbowker :' + nick + ' ( ' + cloak + ' ) has left ' + mainchan + '.\r\n' );
                    irc.send ( 'PRIVMSG ##WikipediaWelcomer :' + nick + ' ( ' + cloak + ' ) has left ' + mainchan + '.\r\n' );
                    reset.put('0');
            elif data.find ( '?quit' ) != -1: # Check for a quit order
                if data.find ( 'wikipedia/matthewrbowker' ) != -1:
                    irc.send ( 'PRIVMSG ' + mainchan + ' :I am shutting down in 5 seconds.\r\n' );  # Shutting down notifications
                    irc.send ( 'PRIVMSG ##matthewrbowker :I am shutting down in 5 seconds.\r\n' ); 
                    irc.send ( 'PRIVMSG ##WikipediaWelcomer :I am shutting down in 5 seconds.\r\n' );
                    reset.put('0');
                    site=mwclient.Site('en.wikipedia.org');
                    site.login('WikiWelcomer','editor')
                    page = site.Pages['User:WikiWelcomer/Control']
                    save = page.save('off','Shutting off bot, requested on [[WP:IRC |IRC]] (bot)');
                    time.sleep(5);
                    irc.send ( 'QUIT : Requested by operator\r\n' );
                    time.sleep(2);
                    sys.exit()
            elif data.find ('?threadcount') != -1:
                user = data.split() [ 0 ] # Split down to just the user
                user = str(user) # Convert the variable to a string
                user = user.replace ( ':', '', 1) # Get rid of the colon at the beginning
                nick = user.split ( '!' ) [ 0 ] # Right, let's go down and remove the IP information
                nick = str(nick) # Convert the variable to a string
                chan = data.replace(':' + user + ' PRIVMSG ','',1)
                chan = chan.split(' :' ) [0]
                chan = str(chan)
                count = threading.active_count()
                count = str(count)
                irc.send ( 'PRIVMSG ' + chan + ' :' + nick + ': There are curently ' + count + ' active threads.\r\n' );
                reset.put('0');
            elif data.find ('?threads') != -1:
                user = data.split() [ 0 ] # Split down to just the user
                user = str(user) # Convert the variable to a string
                user = user.replace ( ':', '', 1) # Get rid of the colon at the beginning
                nick = user.split ( '!' ) [ 0 ] # Right, let's go down and remove the IP information
                nick = str(nick) # Convert the variable to a string
                chan = data.replace(':' + user + ' PRIVMSG ','',1)
                chan = chan.split(' :' ) [0]
                chan = str(chan)
                threads = threading.enumerate()
                threads = str(threads)
                irc.send ( 'PRIVMSG ' + chan + ' :' + nick + ': My currently running threads are: ' + threads + '\r\n' );
                reset.put('0');
            elif data.find ('?about') != -1:
                user = data.split() [ 0 ] # Split down to just the user
                user = str(user) # Convert the variable to a string
                user = user.replace ( ':', '', 1) # Get rid of the colon at the beginning
                nick = user.split ( '!' ) [ 0 ] # Right, let's go down and remove the IP information
                nick = str(nick) # Convert the variable to a string
                chan = data.replace(':' + user + ' PRIVMSG ','',1)
                chan = chan.split(' :' ) [0]
                chan = str(chan)
                irc.send ( 'PRIVMSG ' + chan + ' :' + nick + ': I am ' + botnick + ' ' + version + ', written by Matthew Bowker.  Portions of my framework is based on the mwclient library, written by Bryan Tong Minh.  \r\n' );
                reset.put('0');
            elif data.find ( '!helper' ) != -1:
                if data.find ( 'PRIVMSG ' + mainchan  ) !=-1:
                    user = data.split() [ 0 ] # Split down to just the user
                    user = str(user) # Convert the variable to a string
                    user = user.replace ( ':', '', 1) # Get rid of the colon at the beginning
                    cloak = user.split( '@' ) [1]
                    str(cloak)
                    nick = user.split ( '!' ) [ 0 ] # Right, let's go down and remove the IP information
                    nick = str(nick) # Convert the variable to a string
                    message = data.split ( mainchan ) [1]
                    irc.send ( 'PRIVMSG ##matthewrbowker :' + nick + ' ( ' + cloak + ' ) has asked for help in #wikipedia-en-help.  The message is ' + message + '\r\n' ); 
                    irc.send ( 'PRIVMSG ##WikipediaWelcomer :' + nick + ' ( ' + cloak + ' ) has asked for help in #wikipedia-en-help.  The message is ' + message + '\r\n'  );
                    reset.put('0');
            elif data.find ( '?nick' ) != -1: # Check for a nick order
                if data.find ( 'wikipedia/matthewrbowker' ) != -1:
                    user = data.split() [ 0 ] # Split down to just the user
                    user = str(user) # Convert the variable to a string
                    user = user.replace ( ':','',1) # Get rid of the colon at the beginning
                    nick = user.split ( '!' ) [ 0 ] # Right, let's go down and remove the IP information
                    nick = str(nick) # Convert the variable to a string
                    chan = data.replace(':' + user + ' PRIVMSG ','',1)
                    chan = chan.split(' :' ) [0]
                    chan = str(chan)
                    newnick = data.replace( ':' + user + ' PRIVMSG ' + chan + ' :?nick','');
                    newnick = newnick.replace( '\r\n','');
                    irc.send('NICK ' + newnick + '\r\n');
                    irc.send ( 'PRIVMSG ' + chan + ' :' + nick + ': My new nickname, ' + newnick + ', has been set.\r\n' );
                else:
                   irc.send ( 'PRIVMSG ' + chan + ' :' + nick + ': You do not have permission to change my nickname.\r\n' );
            elif data.find ( '?raw' ) != -1:
                if data.find ( 'wikipedia/matthewrbowker' ) != -1:
                    user = data.split() [ 0 ] # Split down to just the user
                    user = str(user) # Convert the variable to a string
                    user = user.replace ( ':', '', 1) # Get rid of the colon at the beginning
                    nick = user.split ( '!' ) [ 0 ] # Right, let's go down and remove the IP information
                    nick = str(nick) # Convert the variable to a string
                    chan = data.replace(':' + user + ' PRIVMSG ','',1)
                    chan = chan.split(' :' ) [0]
                    chan = str(chan)
                    stuff = data.replace( ':' + user + ' PRIVMSG ' + chan + ' :?raw ','');
                    stuff = stuff.replace( '\r\n','');
                    irc.send( stuff + '\r\n' );
#            elif data.find ('?help' ):
#                    helpfunc = data.replace( ':'+ user + ' PRIVMSG ' + chan + ' :?help ','');
#                    con = sqlite3.connect("sql.toolserver.org")
#                    con.isolation_level = None
#                    cur = con.cursor()
#                    query = "SELECT text FROM `u_Matthewrbowker_WikiWelcomer_help`.`help` WHERE `command`=" + helpfunc + " LIMIT 1;"
#                    cur.execute()
#                    text=cur.fetchone()
#                    user = data.split() [ 0 ] # Split down to just the user
#                    user = str(user) # Convert the variable to a string
#                    user = user.replace ( ':', '', 1) # Get rid of the colon at the beginning
#                    nick = user.split ( '!' ) [ 0 ] # Right, let's go down and remove the IP information
#                    nick = str(nick) # Convert the variable to a string
#                    chan = data.replace(':' + user + ' PRIVMSG ','',1)
#                    chan = chan.split(' :' ) [0]
#                    chan = str(chan)
#                    irc.send ('PRIVMSG ' + chan + ' :' + nick + ':Showing help for function "' + helpfunc + '": ' + text + '\r\n')
            elif data.find ( botnick ) != -1:
                if data.find ( 'PRIVMSG ' + mainchan ) != -1:
                    irc.send ( 'PRIVMSG ' + mainchan + ' ::D \r\n' );
                elif data.find ( 'PRIVMSG ##matthewrbowker' ) != -1:
                    irc.send ( 'PRIVMSG ##matthewrbowker ::D \r\n' );
                elif data.find ( 'PRIVMSG ##wikipediawelcomer' ) != -1:
                    irc.send ( 'PRIVMSG ##wikipediawelcomer ::D \r\n' );
                reset.put('0');
        except:
            irc.send( 'QUIT :Quit: This bot has encountered an error and needs to close.\r\n' );
            time.sleep(2)
            sys.exit();

def checkingwiki():
    while True:
        try:
            time.sleep(5)
            urllib.urlretrieve('http://en.wikipedia.org/wiki/User:WikiWelcomer/Control?action=raw', 'status.wwbot')
            f = open('status.wwbot')
            status = f.read()
            f.close()
            if status == 'off':
                irc.send('QUIT : My status page has been set to off.\r\n');
                sys.exit()
        except:
            irc.send('QUIT : An error has occured with the wiki check.  Exiting.');


first = threading.Thread(target=pingingout)
second = threading.Thread(target=datarecieve)
third = threading.Thread(target=checkingwiki)

first.daemon = True
second.daemon = True
third.daemon = True

first.start()
second.start()
third.start()

while True:
    threadnum = threading.active_count()
    threadnum = int(threadnum)
    if threadnum != 4:
        sys.exit()
    time.sleep(1)
