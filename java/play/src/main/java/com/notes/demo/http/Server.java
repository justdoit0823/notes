package com.notes.demo.http;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

public class Server {

  public static void main(String[] args) throws IOException {
    int port = 0;
    if (args.length >= 1) {
      port = Integer.parseInt(args[0]);
    }

    HttpServer server = HttpServer.create(new InetSocketAddress("127.0.0.1", port), 128);
    server.createContext("/", new IndexHandler());
    server.setExecutor(null);

    System.out.println("running server at " + server.getAddress());
    server.start();
  }

  static class IndexHandler implements HttpHandler {

    @Override
    public void handle(HttpExchange t) throws IOException {

      String response = "Hello world.";
      t.sendResponseHeaders(200, response.length());
      OutputStream os = t.getResponseBody();
      os.write(response.getBytes());
      os.close();
    }
  }
}
