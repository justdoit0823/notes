package com.notes.demo.validation;

import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class ConcurrentMutateValidation {

  public static void main(String[] args) {
    int threadNum = 10;
    int opNum = 100;
    String counterType;

    if (args.length < 1) {
      System.out.println("Counter type is needed.");
      return;
    }

    counterType = args[0];
    if (args.length > 1) threadNum = Integer.parseInt(args[1]);
    if (args.length > 2) opNum = Integer.parseInt(args[2]);

    CounterOperator c;
    if (counterType.equals("sync")) {
      c = new SyncCounter();
    } else {
      c = new VolatileCounter();
    }

    final int testOpNum = opNum;
    List<MutateThread> threads = IntStream.range(0, threadNum).boxed().map(i -> new MutateThread(c, testOpNum)).collect(
        Collectors.toList());
    threads.forEach(MutateThread::start);

    synchronized (c) {
      c.start();
      c.notifyAll();
    }

    List<Boolean> ret = threads.stream().map(t -> {
      try {
        t.join();
        return true;
      } catch (InterruptedException e) {
        System.out.println(e);
        return false;
      }
    }).collect(Collectors.toList());

    System.out.println("success task num:" + ret.stream().filter(Boolean::booleanValue).count() + ", mutated value:" + c.getValue());
  }

  interface CounterOperator {

    void start();

    boolean isStarted();

    void add();

    int getValue();

  }

  static class SyncCounter implements CounterOperator {

    private volatile boolean started = false;
    private int cnt = 0;

    public void start() {
      started = true;
    }

    public boolean isStarted() {
      return started;
    }

    public synchronized void add() {
      cnt += 1;
    }

    public int getValue() {
      return cnt;
    }

  }

  static class VolatileCounter implements CounterOperator {

    private volatile boolean started = false;
    private volatile int cnt = 0;

    public void start() {
      started = true;
    }

    public boolean isStarted() {
      return started;
    }

    public void add() {
      cnt += 1;
    }

    public int getValue() {
      return cnt;
    }

  }

  static class MutateThread extends Thread {

    private CounterOperator c;
    private int num = 0;

    MutateThread(CounterOperator c, int n) {
      this.c = c;
      num = n;
    }

    public void run() {

      synchronized (c) {
        while (!c.isStarted()) {
          try {
            c.wait();
          } catch (Exception e) {
            System.out.println(e);
          }
        }
      }

      for (int i = 0; i < num; i++) c.add();
    }

  }

}
