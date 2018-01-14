
import java.net.*;
import java.io.*;
import java.net.HttpURLConnection;


class IpInfo {

    public static void main(String[] args) {

	String urlString = new String("");
	if(args.length >= 1) urlString = "https://ipinfo.io/" + args[0] + "/json";
	else urlString = "https://ipinfo.io/json";

	try {

	    URL url = new URL(urlString);
	    HttpURLConnection conn = (HttpURLConnection)url.openConnection();
	    conn.setRequestMethod("GET");
	    conn.setRequestProperty("User-Agent", "java/ipinfo");

	    BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream()));
	    String inputLine;
	    while ((inputLine = in.readLine()) != null) 
		System.out.println(inputLine);
	    in.close();

	}
	catch (MalformedURLException e) {

	    System.out.println(e);

	}
	catch (IOException e) {

	    System.out.println(e);

	}

    }

}
