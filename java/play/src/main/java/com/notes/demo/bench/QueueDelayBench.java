package com.notes.demo.bench;

import java.util.Arrays;
import java.util.concurrent.Callable;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.List;
import java.util.LinkedList;
import java.util.stream.IntStream;
import java.util.stream.Collectors;
import java.util.concurrent.Future;

public class QueueDelayBench {

  public static void main(String[] args) {
    int concurrence = Integer.parseInt(args[0]);
    int num = Integer.parseInt(args[1]);
    int factor = Integer.parseInt(args[2]);
    run(concurrence, num, factor);
  }

  public static void run(int concurrence, final int num, final int factor) {
    ExecutorService executorService = Executors.newFixedThreadPool(concurrence);
    ExecutorService middleExecutor = Executors.newFixedThreadPool(concurrence * factor);

    List<Callable<List<Long>>> tasks = IntStream.rangeClosed(1, concurrence).boxed().map(i -> (Callable<List<Long>>) () -> {
      int testNum = num;
      final ConcurrentLinkedQueue<Long> durationQueue = new ConcurrentLinkedQueue<>();

      while (testNum-- > 0) {
        final long startTs = System.nanoTime();

        List<Future<Long>> futures = IntStream.rangeClosed(1, factor).mapToObj(n -> middleExecutor.submit(() -> {
          long startExecutionTs = System.nanoTime();
          durationQueue.add(startExecutionTs - startTs);
          TimeUnit.MILLISECONDS.sleep(3);

          return (startExecutionTs - startTs);
        })).collect(Collectors.toList());

        TimeUnit.MILLISECONDS.sleep(5);
        futures.forEach(f -> {
          if (!f.isDone()) {
            return;
          }

          try {
            f.get(0, TimeUnit.MILLISECONDS);
          } catch (Exception e) {
            return;
          }
        });
      }

      Long[] t = new Long[1];
      return Arrays.asList(durationQueue.toArray(t));
    }).collect(Collectors.toList());

    List<Future<List<Long>>> futures;
    long startTs = System.nanoTime();
    try {
      futures= executorService.invokeAll(tasks);
    } catch (InterruptedException e) {
      System.out.println(e);
      return;
    }
    long stopTs = System.nanoTime();

    List<Long> delays = futures.stream().map(f -> {
      try {
        return f.get();
      } catch (Exception e) {
        System.out.println(e);
        return new LinkedList<Long>();
      }
    }).collect(Collectors.toList()).stream().flatMap(List::stream).sorted().collect(Collectors.toList());

    final long totalTs = delays.stream().mapToLong(Long::longValue).sum();

    System.out.println("duration:" + (stopTs - startTs) / 1000000.0);
    System.out.println("total tasks:" + delays.size() + ",delay mean:" + totalTs / 1000000.0 / delays.size() + ",delay p99:" + delays.get((int)(delays.size() * 0.99)) / 1000000.0);

    System.exit(0);
  }

}
