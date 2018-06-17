
import java.lang.*;
import java.io.*;
import java.nio.charset.*;
import java.nio.file.*;
import javax.json.*;


public class TestJson {

    public static void main(String[] args) {

	try {
	    Path path = FileSystems.getDefault().getPath(".", "data.json");
	    BufferedReader reader = Files.newBufferedReader(path, StandardCharsets.UTF_8);
	    JsonReader jsonReader = Json.createReader(reader);

	    JsonObject obj = jsonReader.readObject();
	    String firstName = obj.getJsonString("firstName").toString();
	    System.out.println(firstName);

	} catch (IOException e) {
	    System.out.println(e);
	}

    }
}
