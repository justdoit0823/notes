package com.notes.demo.bench;

import com.notes.demo.task.SimpleTaskResult;
import com.notes.demo.task.TaskResult;
import com.notes.demo.task.TaskRunner;
import java.util.Queue;
import java.util.concurrent.Callable;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.TimeUnit;
import java.util.List;
import java.util.LinkedList;

import java.util.concurrent.atomic.LongAdder;
import java.util.stream.IntStream;
import java.util.stream.Collectors;
import java.util.concurrent.Future;

public class CascadeThreadPoolBench {

  private static final LongAdder successNum = new LongAdder();
  private static final Queue<Long> durationQueue = new ConcurrentLinkedQueue<Long>();

  public static void main(String[] args) {
    int concurrence = Integer.parseInt(args[0]);
    int num = Integer.parseInt(args[1]);
    run(concurrence, num);
  }

  public static void run(int concurrence, final int num) {

    ExecutorService middleExecutor = Executors.newFixedThreadPool(concurrence * 7);
    ExecutorService outerExecutor = Executors.newFixedThreadPool(concurrence * 7);

    List<Callable<TaskResult<Boolean>>> tasks = IntStream.range(0, concurrence).boxed().map(i -> (Callable<TaskResult<Boolean>>) () -> {
      int testNum = num;
      int okNum = 0;
      long startTs = System.nanoTime();
      List<Long> durations = new LinkedList<>();
      while (testNum-- > 0) {
        long taskStartTs = System.nanoTime();
        boolean ok = false;
        List<Future<Integer>> futures = IntStream.range(0, 7).mapToObj(n -> middleExecutor.submit(() -> {
          Future<Integer> future = outerExecutor.submit(() -> {
            try {
              Thread.sleep(5 + ThreadLocalRandom.current().nextInt(7));
            } catch (InterruptedException ignore) {

            }

            return 1;
          });

          try {
            return future.get(14, TimeUnit.MILLISECONDS);
          } catch (Exception ignore) {
          }

          return 0;
        })).collect(Collectors.toList());

        int timeout = 15;
        while (timeout > 0) {
          ok = futures.stream().map(f -> {
            if (!f.isDone()) {
              return 0;
            }

            try {
              return f.get(0, TimeUnit.MILLISECONDS);
            } catch (Exception e) {
              return 0;
            }
          }).allMatch(b -> b == 1);

          if (ok) {
            break;
          } else {
            TimeUnit.MILLISECONDS.sleep(timeout >= 2 ? 2: timeout);
            timeout -= 2;
          }
        }

        if (ok) {
          long stopTs = System.nanoTime();
          okNum++;
          durations.add((stopTs - taskStartTs) / 1000000);
        }
      }

      successNum.add(okNum);
      durations.forEach(durationQueue::offer);
      return new SimpleTaskResult<>(true, (System.nanoTime() - startTs));

    }).collect(Collectors.toList());

    long startTs = System.nanoTime();
    TaskRunner<Boolean> taskRunner = new TaskRunner<>(tasks, concurrence);
    taskRunner.run();
    long stopTs = System.nanoTime();

    List<Long> totalDurations = new LinkedList<>(durationQueue.stream().sorted().collect(Collectors.toList()));

    System.out.println("duration:" + (stopTs - startTs) / 1000000L + ", ok num:" + successNum.longValue());
    System.out.println("performance:" + "mean:" + totalDurations.stream().mapToLong(Long::longValue).sum() / successNum.longValue() + ",p90:" + totalDurations.get((int)(successNum.longValue() * 0.9)) + ", p99:" + totalDurations.get((int)(successNum.longValue() * 0.99)));
    System.out.println("durations" + totalDurations.subList(0, 10));

    System.exit(0);
  }

}
