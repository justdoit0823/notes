

public class SumLambda {

    public static void main(String[] args) {

	int a = 1;
	int b = 2;
	int c = (int a, int b) -> {return a + b;}(a, b);

	System.out.printf("%d + %d = %d.\n", a, b, c);

    }
}
