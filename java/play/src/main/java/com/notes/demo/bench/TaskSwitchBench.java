package com.notes.demo.bench;

import java.util.List;
import java.util.concurrent.*;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class TaskSwitchBench {

  public static void main(String[] args) {
    final int concurrence = Integer.parseInt(args[0]);
    final int roundNum = Integer.parseInt(args[1]);
    int timeout = 5;
    if (args.length > 2) {
      timeout = Integer.parseInt(args[2]);
    }
    final int probeTimeout = timeout;

    ExecutorService executorService = Executors.newFixedThreadPool(concurrence);
    ExecutorService innerExecutor = Executors.newFixedThreadPool(concurrence);

    List<Callable<Integer>> allTasks =
        IntStream.range(0, concurrence)
            .boxed()
            .map(
                (i) ->
                    (Callable<Integer>)
                        () -> {
                          int num = roundNum;
                          final long n = System.nanoTime();
                          while (num > 0) {
                            Future<Integer> future =
                                innerExecutor.submit(
                                    () -> {
                                      try {
                                        TimeUnit.MICROSECONDS.sleep(probeTimeout);
                                      } catch (InterruptedException e) {

                                      }

                                      return 1;
                                    });

                            try {
                              future.get();
                            } catch (Exception e) {

                            }

                            num--;
                          }
                          return 1;
                        })
            .collect(Collectors.toList());

    long startTs = System.nanoTime();
    try {
      executorService.invokeAll(allTasks);
    } catch (InterruptedException e) {
      System.out.println(e);
    }

    long stopTs = System.nanoTime();
    long duration = (stopTs - startTs) / 1000000;
    System.out.println("concurrence:" + concurrence + ", test num:" + roundNum + ", duration:" + duration + "ms");
    System.out.println("probe timeout:" + probeTimeout + ", task per second:" + concurrence * roundNum / (duration / 1000.0));

    System.exit(0);
  }
}
