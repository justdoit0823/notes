package com.notes.demo.http;

import java.net.*;
import java.io.*;
import java.net.HttpURLConnection;

public class IpInfo {

  public static void main(String[] args) {

    String urlString = "https://ipinfo.io/json";
    if (args.length >= 1) {
      urlString = "https://ipinfo.io/" + args[0] + "/json";
    }

    try {
      URL url = new URL(urlString);
      HttpURLConnection conn = (HttpURLConnection) url.openConnection();
      conn.setRequestMethod("GET");
      conn.setRequestProperty("User-Agent", "java/ipinfo");

      BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream()));
      String inputLine;
      while ((inputLine = in.readLine()) != null) System.out.println(inputLine);
      in.close();

    } catch (IOException e) {
      System.out.println(e);
    }
  }
}
