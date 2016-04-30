package Includes;

public class config {
    private String wikiUsername;
    private String wikiPassword;
    private String wikiUrl;
    private boolean debug;
    private int exitCode;

    public config() {
        this.debug = false;
        this.wikiUsername = "";
        this.wikiPassword = "";
        this.wikiUrl = "";
        this.exitCode = 0;

    }

    public String getWikiUsername() {
        return wikiUsername;
    }

    public void setWikiUsername(String wikiUsername) {
        this.wikiUsername = wikiUsername;
    }

    public String getWikiPassword() {
        return wikiPassword;
    }

    public void setWikiPassword(String wikiPassword) {
        this.wikiPassword = wikiPassword;
    }

    public String getWikiUrl() {
        return wikiUrl;
    }

    public void setWikiUrl(String wikiUrl) {
        this.wikiUrl = wikiUrl;
    }

    public void setDebug(boolean value) {
        debug = value;
    }

    public boolean getDebug() {
        return debug;
    }

    public int getExitCode() {
        return exitCode;
    }

    public void setExitCode(int exitCode) {
        this.exitCode = exitCode;
    }
}