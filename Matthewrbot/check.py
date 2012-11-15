#! usr/bin/python

# Matthewrbot's check module
# This module checks whether the bot is enabled on-wiki.  It will start Matthewrbot.py.  It should be initialized using Cron.

import urllib;
import os;

urllib.urlretrieve("http://en.wikipedia.org/wiki/User:Matthewrbot/Control?action=raw","main.mbot");
urllib.urlretrieve("http://en.wikipedia.org/wiki/User:Matthewrbot/Control/1?action=raw","task.mbot");

f1 = open('main.mbot');
status1 = f1.read();
f1.close();

f2 = open('task.mbot');
status2 = f2.read();
f2.close();

if (status1=='on' and status2 == 'on'):
    os.system("python Matthewrbot.py");
else:
    print "File is set to off, exiting";
