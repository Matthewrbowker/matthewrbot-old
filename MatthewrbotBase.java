import jwiki.core.*;
import Includes.*;
import Pods.*;

public class MatthewrbotBase{
    public static void main(String[] args) {
        config con = new config();
        Wiki wiki;
        logging log;
        ircd irc;
        queuep queue;

        con.setDebug(true);

        log = new logging();

        try {
            log.string("Hello, World!");
            // wiki = new Wiki(con.getWikiUsername(), con.getWikiPassword(), con.getWikiUrl()); // login
            queue = new queuep();

            queue.put("##matthewrbot", "1. This is a test message");
            queue.put("##matthewrbowker", "1. This is a test message");
            queue.put("##matthewrbot", "2. This is a test message");
            queue.put("##matthewrbot", "3. This is a test message");
            queue.put("##matthewrbot", "4. This is a test message");
            queue.put("##matthewrbot", "5. This is a test message");
            queue.put("##matthewrbot", "6. This is a test message");
            queue.put("##matthewrbot", "7. This is a test message");
            queue.put("##matthewrbot", "8. This is a test message");
            queue.put("##matthewrbot", "9. This is a test message");

            irc = new ircd(con, log, queue);
            irc.registerChannel("##matthewrbot");
            irc.registerChannel("##matthewrbowker");

            Thread.sleep(100);

            irc.run();

        }
        catch (Throwable e) {
            con.setExitCode(1);
            log.error(e.getMessage());
            if (con.getDebug()) e.printStackTrace();
        }
        finally {
            log.string("Process exiting with code " + con.getExitCode());
            log.string("Shutting down...");
            // Do stuff here...
            log.string("Complete.");
        }

        System.exit(con.getExitCode());
    }
}