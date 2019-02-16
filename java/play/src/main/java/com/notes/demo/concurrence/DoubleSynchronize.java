package com.notes.demo.concurrence;

import java.util.stream.IntStream;

public class DoubleSynchronize {

  private static final Counter counter = new Counter();

  public static void main(String[] args) {

    FooThread ft1 = new FooThread();
    FooThread ft2 = new FooThread();

    ft1.setRecursive(true);
    ft2.setRecursive(true);

    ft1.start();
    ft2.start();

    try{
      ft1.join();
      ft2.join();
    } catch (Exception e) {
      System.out.println(e);
    }

    System.out.println("counter value " + counter.count);
  }

  static class FooThread extends Thread {

    private boolean recursive = false;

    public void setRecursive(boolean recursive) {
      this.recursive = recursive;
    }

    public void run() {
      IntStream.range(0, 10000).forEach(i -> counter.add(recursive));
    }
  }

  static class Counter {

    private int count = 0;

    private void add(boolean recursive) {
      if (recursive) {
        synchronized (this) {
          count += 1;

          add(false);
        }
      } else {
        synchronized (this) {
          count += 1;
        }
      }
    }
  }
}
