
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;


public class Server {

    public static void main(String[] args) throws Exception {

	if(args.length < 1){
	    System.out.println("invalid server port.");
	    return;
	}

	HttpServer server = HttpServer.create(new InetSocketAddress(Integer.parseInt(args[0])), 0);
	server.createContext("/", new IndexHandler());
	server.setExecutor(null);
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
