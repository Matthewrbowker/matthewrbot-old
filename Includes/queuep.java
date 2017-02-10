package Includes;

public class queuep {
    String[][] queue;
    int numItems;

    public queuep() {
        queue = new String[100][2];

        numItems = -1;
    }

    public String[] get() {
        String[] retVal;

        retVal = this.queue[0];

        for(int i = 1; i <= 99; i++) {
            this.queue[i-1] = this.queue[i];
        }

        numItems--;

        return retVal;
    }

    public void put(String channel, String message) {
        numItems++;
        this.queue[numItems][0] = channel;
        this.queue[numItems][1] = message;
    }

    public boolean hasItems() {
        return numItems > -1;
    }

}
