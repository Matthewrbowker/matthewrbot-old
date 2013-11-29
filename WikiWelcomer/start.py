#! usr/bin/python

# WikiWelcomer's start module
# This module checks whether the bot is enabled on-wiki.  It will start WikipediaWelcomer.py.  It should be initialized using Cron.

import urllib;
import os;

urllib.urlretrieve("http://en.wikipedia.org/wiki/User:WikiWelcomer/Control?action=raw","status.wwbot");

ff = open('status.wwbot');
status1 = ff.read();
ff.close();

processname = 'WikipediaWelcomer.py'

for line in os.popen("ps -u matthewrbowker"):
    fields = line.split()
    pid = fields[0]
    process = fields[3]

if (status1=='on'):
    if process.find(processname) > 0:
        print "Doing nothing, process found!";
    else:
        os.system("nohup python $HOME/Bots/WikipediaWelcomer/WikipediaWelcomer.py > /home/matthewrbowker/public_html/logs/wikiwelcomer/main.out");
else:
    print "File is set to off, exiting";
