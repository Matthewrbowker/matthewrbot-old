import jwiki.core.*;

import java.net.URL;
import java.net.URLClassLoader;

public class MatthewrbotBase {

    public static void main(String[] args) {
        // Prints "Hello, World" to the terminal window.
        System.out.println("Hello, World");

        //Wiki wiki = new Wiki("Username", "Password", "en.wikipedia.org"); // login

        ClassLoader cl = ClassLoader.getSystemClassLoader();

        URL[] urls = ((URLClassLoader)cl).getURLs();

        for(URL url: urls){
            System.out.println(url.getFile());
        }
    }


}