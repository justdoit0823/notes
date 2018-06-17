

class Resolver {

    public void showName() {
	System.out.println("Resolver...");
    }
}


public class TestNullObjectMethod {

    public static void main(String[] args) {
	Resolver r1 = null;
	r1.showName();
    }
}
