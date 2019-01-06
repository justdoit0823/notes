package com.notes.demo.bench;

import com.notes.demo.task.SimpleTaskResult;
import com.notes.demo.task.TaskResult;
import com.notes.demo.task.TaskRunner;
import java.util.Arrays;
import java.util.Collection;
import java.util.concurrent.Callable;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.List;
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
    ExecutorService middleExecutor = Executors.newFixedThreadPool(concurrence * factor);
    List<Callable<TaskResult<List<Long>>>> tasks = IntStream.rangeClosed(1, concurrence).boxed().map(i -> (Callable<TaskResult<List<Long>>>) () -> {
      int testNum = num;
      long startTs = System.nanoTime();
      final ConcurrentLinkedQueue<Long> durationQueue = new ConcurrentLinkedQueue<>();

      while (testNum-- > 0) {
        final long taskStartTs = System.nanoTime();

        List<Future<Long>> futures = IntStream.rangeClosed(1, factor).mapToObj(n -> middleExecutor.submit(() -> {
          long startExecutionTs = System.nanoTime();
          durationQueue.add(startExecutionTs - taskStartTs);
          TimeUnit.MILLISECONDS.sleep(3);

          return (startExecutionTs - taskStartTs);
        })).collect(Collectors.toList());

        TimeUnit.MILLISECONDS.sleep(5);
        futures.forEach(f -> {
          if (!f.isDone()) {
            return;
          }

          try {
            f.get(0, TimeUnit.MILLISECONDS);
          } catch (Exception ignore) {
          }
        });
      }

      long stopTs = System.nanoTime();
      Long[] t = new Long[1];
      return new SimpleTaskResult<>(Arrays.asList(durationQueue.toArray(t)), stopTs - startTs);
    }).collect(Collectors.toList());

    TaskRunner<List<Long>> taskRunner = new TaskRunner<>(tasks, concurrence);
    List<TaskResult<List<Long>>> results = taskRunner.run();

    List<Long> delayDurations = results.stream().map(TaskResult::getTaskResult).flatMap(Collection::stream).collect(Collectors.toList());
    long totalDelayDuration = delayDurations.stream().mapToLong(Long::longValue).sum();
    System.out.println("queue delay mean time " + totalDelayDuration / 10e6 / delayDurations.size());

    System.exit(0);
  }

}
