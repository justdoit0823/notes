
import java.util.ArrayList;


public class TestFinal {

    public static void main(String[] args) {

	final int num = 10;
	final ArrayList<Integer> itemList = new ArrayList<Integer>();

	// num = 100;

	for(int i = 0; i < num; i++) {
	    itemList.add(i);
	}

	System.out.println(itemList);

    }

}
