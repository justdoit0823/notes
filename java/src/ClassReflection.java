

public class ClassReflection {

    public static void main(String[] args) {
	int x = 10000;
	int x2 = 1;
	int x3 = x;
	String y = "hahaha";

	double k = 9.87;
	int k1 = (int)k;

	System.out.println(x);
	x += 1;
	System.out.println(x);
	x = x + 1;
	System.out.println(x);

	Object z = new Object();
	for(int i = 0; i < 10; i++) {
	    System.out.println(i);
	}
	System.out.println(ClassReflection.class);
	System.out.println(Integer.class);
    }

}
