import os;
import oursql;
import mwclient;
from sites import pages,section;
import urllib;
#from functions import sort;

import config.local.inc.py # Get local configuration

#Define the database and connect

db = oursql.connect(db='u_matthewrbowker_articlerequest',
        host="sql.toolserver.org",
        read_default_file=os.path.expanduser("~/.my.cnf"),
        charset=None,
        use_unicode=False
)

curs = db.cursor();

#OK, now for MWclient
site = mwclient.Site('en.wikipedia.org');
site.login(uname,password);

#Query the database
result = curs.execute("SELECT * FROM `requests` WHERE 1");

#Put the data on the wiki
while (1):
    row = curs.fetchone();
    if row == None:
        break
    page = pages(row[3],row[4],row[5],row[1]);
    sec = section(row[3],row[4],row[5],row[1]);
    pageurl = page.replace(' ','_');
    if sec == -1:
        curs.execute("INSERT INTO `archive` VALUES ('" + str(row[0]) + "','" + str(row[1]) + "','" + str(row[2]) + "','"+ str(row[3]) + "','" str(row[4]) + "','" + str(row[5]) + "','" + str(row[6]) + "','" + str(row[7]) + "','Unable to add to Wikipedia - Undefined section')");
        curs.execute("DELETE FROM `requests` WHERE `id`='" + str(row[0]) + "' LIMIT 1");
        continue
    editpage = site.Pages[page];
    urllib.urlretrieve("http://en.wikipedia.org/wiki/" + pageurl + "?action=raw",'main.mfile');
    urllib.urlretrieve("http://en.wikipedia.org/wiki/" + pageurl + "?action=raw&section=" + sec, 'section.mfile');
    mpf = open('main.mfile');
    mainpage = mpf.read();
    mpf.close
    sf = open('section.mfile');
    old = sf.read();
    sf.close
    new = old;
    new = new + "\n*[[" + row[1] + "]] - " + row[2];
    if row[6] != '':
        new = new + "<small> - Requested by {{user|" + row[6] + "}}</small>";
    new = new + "<!-- Request ID# " + str(row[0]) + ", requested on " + str( row[7]) + " -->";
#    print new;
#    new = sort(new);
    mainpage = mainpage.replace(old,new)
    save = editpage.save(mainpage,"Adding request ID# " + str(row[0]) + " ([[WP:BOT|bot]])");
    crs.execute("INSERT INTO `archive` VALUES ('" + str(row[0]) + "','" + str(row[1]) + "','" + str(row[2]) + "','"+ str(row[3]) + "','" str(row[4]) + "','" + str(row[5]) + "','" + str(row[6]) + "','" + str(row[7]) + "','Added to Wikipedia')"); 
    curs.execute("DELETE FROM `requests` WHERE `id`='" + str(row[0]) + "' LIMIT 1");
    print "request #" + str(row[0]) + " added!";


os.remove('main.mfile');
os.remove('section.mfile');

exit();

# row[0] is the request ID number
# row[1] is the subject
# row[2] is the description
# row[3] is the category
# row[4] is the sub-category
# row[5] is the sub-sub-category
# row[6] is the username
# row[7] is the requeset date
