package Includes;

public class logging {
    private int lastDate;

    public void string(String message) {
        System.out.println(message);
    }

    public void error(String message) {
        string("ERROR: " + message);
    }
}
