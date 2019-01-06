package com.notes.demo.lang;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.IntStream;

public class FinalObjectModifier {

  public static void main(String[] args) {

    final int num = 10;
    final List<Integer> itemList = new ArrayList<>();

    IntStream.range(0, num)
        .boxed()
        .forEach(
            i -> {
              itemList.add(i);
            });

    System.out.println(itemList);
  }
}
