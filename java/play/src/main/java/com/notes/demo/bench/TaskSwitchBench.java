package com.notes.demo.bench;

import com.notes.demo.task.SimpleTaskResult;
import com.notes.demo.task.TaskResult;
import com.notes.demo.task.TaskRunner;
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

    ExecutorService innerExecutor = Executors.newFixedThreadPool(concurrence);
    List<Callable<TaskResult<Integer>>> allTasks = IntStream.range(0, concurrence * roundNum)
        .boxed()
        .map(
            (i) ->
                (Callable<TaskResult<Integer>>)
                    () -> {
                      long startTs = System.nanoTime();
                      Future<Integer> future =
                          innerExecutor.submit(
                              () -> {
                                try {
                                  TimeUnit.MICROSECONDS.sleep(probeTimeout);
                                } catch (InterruptedException ignore) {

                                }

                                return 1;
                              });

                      try {
                        future.get();
                      } catch (Exception ignore) {
                      }

                      long stopTs = System.nanoTime();
                      return new SimpleTaskResult<>(1, (stopTs - startTs));
                    })
        .collect(Collectors.toList());

    TaskRunner<Integer> taskRunner = new TaskRunner<>(allTasks, concurrence);
    taskRunner.run();

    System.exit(0);
  }
}
