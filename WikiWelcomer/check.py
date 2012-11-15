#!/usr/bin/env python
import os
import signal

# Change this to your process name
processname = 'WikipediaWelcomer.py'

for line in os.popen("ps -u matthewrbowker"):
    fields = line.split()
    pid = fields[0]
    process = fields[3]

if process.find(processname) > 0:
    exit();
else:
    os.system("nohup python $HOME/Bots/WikipediaWelcomer/start.py > /home/matthewrbowker/public_html/logs/wikiwelcomer/check.out");
    exit();
