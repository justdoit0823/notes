
import java.lang.reflect.*;
import java.util.HashMap;


@interface MethodAnnotation {

    String method() default "GET";
    String[] requiredFields();

}


class Request {

    @MethodAnnotation (
	method = "POST",
	requiredFields = {"A", "B", "C"}
    )
    public boolean process(String path, String method, HashMap<String, String> data) {
	Class<Request> cls = Request.class;
	MethodAnnotation a = cls.getAnnotation(MethodAnnotation.class);
	if(!method.equals(a.method())) return false;

	for(String f: a.requiredFields()) {
	    if(data.get(f) == null) return false;
	}

	return true;
    }
}


public class RequestAnnotation {

    public static void main(String[] args) {

	Request req1 = new Request();
	HashMap<String, String> data1 = new HashMap<String, String>();
	assert !req1.process("/", "GET", data1);

	Request req2 = new Request();
	HashMap<String, String> data2 = new HashMap<String, String>();
	data2.put("A", "1");
	data2.put("B", "1");
	data2.put("C", "1");
	assert !req2.process("/", "GET", data2);

	Request req3 = new Request();
	HashMap<String, String> data3 = new HashMap<String, String>();
	data3.put("A", "1");
	assert !req3.process("/", "POST", data3);

	Request req4 = new Request();
	HashMap<String, String> data4 = new HashMap<String, String>();
	data4.put("A", "1");
	data4.put("B", "1");
	data4.put("C", "1");
	assert !req4.process("/", "POST", data4);

	System.out.println("assert done.");

    }
}
