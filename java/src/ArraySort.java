
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Random;
import java.time.*;


class ArraySort {

    public static int randInt(int min, int max) {

	Random rand = new Random();

	return rand.nextInt((max - min) + 1) + min;

    }

    public static void main(String[] args) {

	int elementNum = 0;

	if(args.length < 1) {

	    System.out.println("Element number is needed.");
	    return;

	}

	elementNum = Integer.parseInt(args[0]);
	System.out.printf("Test %d emelemts.\n", elementNum);

	ArrayList<Integer> elementList = new ArrayList<Integer>();
	Integer[] intList = new Integer[elementNum];
	for(int i = 0; i < elementNum; i++) elementList.add(randInt(1, 100000));

	ZoneId zoneId = ZoneId.systemDefault();

	LocalDateTime startTime = LocalDateTime.now();
	Arrays.sort(elementList.toArray());
	LocalDateTime stopTime = LocalDateTime.now();
	long duration = stopTime.atZone(zoneId).toInstant().toEpochMilli() - startTime.atZone(zoneId).toInstant().toEpochMilli();
	System.out.printf("sorting duration %d ms.\n", duration);

	LocalDateTime startTime1 = LocalDateTime.now();
	Arrays.parallelSort(elementList.toArray(intList));
	LocalDateTime stopTime1 = LocalDateTime.now();
	long duration1 = stopTime1.atZone(zoneId).toInstant().toEpochMilli() - startTime1.atZone(zoneId).toInstant().toEpochMilli();
	System.out.printf("sorting duration %d ms.\n", duration1);

    }

}
