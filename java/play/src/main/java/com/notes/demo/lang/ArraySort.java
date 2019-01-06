package com.notes.demo.lang;

import java.util.Arrays;
import java.util.List;
import java.util.concurrent.ThreadLocalRandom;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

class ArraySort {

  public static void main(String[] args) {

    int elementNum = 200000;
    if (args.length >= 1) {
      elementNum = Integer.parseInt(args[0]);
    }

    System.out.println("Test " + elementNum + " elements.");
    List<Integer> elementList =
        IntStream.range(0, elementNum)
            .boxed()
            .map(i -> ThreadLocalRandom.current().nextInt(100000))
            .collect(Collectors.toList());

    long startTs = System.nanoTime();
    Arrays.sort(elementList.toArray());
    long stopTs = System.nanoTime();
    System.out.println("sorting duration " + (stopTs - startTs) / 1e6 + " ms");

    Integer[] inArray = new Integer[1];
    startTs = System.nanoTime();
    Arrays.parallelSort(elementList.toArray(inArray));
    stopTs = System.nanoTime();
    System.out.println("sorting duration " + (stopTs - startTs) / 1e6 + "ms");
  }
}
