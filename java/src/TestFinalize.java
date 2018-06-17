
import java.util.concurrent.TimeUnit;


class MemoryObject {

    private int size;

    public MemoryObject(int size) {
	this.size = size;
    }

    public String detail() {
	return size + "KB";
    }
    
    public void finalize() {
	System.out.println("finalize the object.");
    }

}



public class TestFinalize {

    public static void main(String[] args) {

	MemoryObject m1;

	m1 = new MemoryObject(1000);
	System.out.println(m1.detail());

	m1 = new MemoryObject(2000);
	System.out.println(m1.detail());

	try {
	    TimeUnit.SECONDS.sleep(10);
	} catch (InterruptedException e) {
	    System.out.println(e);
	}

    }
    
}
