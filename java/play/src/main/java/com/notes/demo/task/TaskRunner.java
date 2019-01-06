package com.notes.demo.task;

import java.util.Collections;
import java.util.List;
import java.util.Objects;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.stream.Collectors;

public class TaskRunner<T> {

  private int concurrence;
  private List<Callable<TaskResult<T>>> tasks;

  public TaskRunner(List<Callable<TaskResult<T>>> tasks, int concurrence) {
    this.tasks = tasks;
    this.concurrence = concurrence;
  }

  public List<TaskResult<T>> run() {
    List<Future<TaskResult<T>>> futures;
    ExecutorService executorService = Executors.newFixedThreadPool(concurrence);

    long startTs = System.nanoTime();
    try{
      futures = executorService.invokeAll(tasks);
    } catch (InterruptedException e) {
      reportInterruption(e);
      return Collections.emptyList();
    }

    long stopTs = System.nanoTime();
    long totalDuration = (stopTs - startTs);

    List<TaskResult<T>> results = futures.stream().map(f -> {
      try{
        return f.get();
      } catch (Exception e) {
        return null;
      }
    }).filter(Objects::nonNull).filter(TaskResult::isSuccess).collect(Collectors.toList());

    reportSuccess(tasks.size(), totalDuration, results);

    return results;
  }

  private void reportInterruption(Exception e) {
    System.out.println("task runner is interrupted, " + e);
  }

  private void reportSuccess(long taskNum, long totalDuration,  List<TaskResult<T>> results) {
    double successRate = results.size() * 1.0 / taskNum;
    List<Long> taskDurations = results.stream().map(TaskResult::getTaskExecutionDuration).sorted().collect(
        Collectors.toList());
    long totalTaskDuration = taskDurations.stream().mapToLong(Long::longValue).sum();
    DurationStatistic taskStatistic = DurationCalculator.compute(taskDurations);

    List<Long> delayDurations = results.stream().map(TaskResult::getTaskDelayDuration).sorted().collect(
        Collectors.toList());
    DurationStatistic delayStatistic = DurationCalculator.compute(delayDurations);

    System.out.println("Total task duration " + totalDuration / 1e6 + ", success num " + results.size() + ", mean time " + totalTaskDuration / 1e6 / taskDurations.size());
    System.out.println("Task concurrence " + concurrence + ", per second " + results.size() / (totalDuration / 1e9) + ", and success rate " + successRate);
    System.out.println("Task time distribution p90 " + taskStatistic.getP90() / 1e6 + ", task p99 " + taskStatistic.getP99() / 1e6 + ", task p999 " + taskStatistic.getP999() / 1e6);
    System.out.println("Delay time distribution p90 " + delayStatistic.getP90() / 1e6 + ", task p99 " + delayStatistic.getP99() / 1e6 + ", task p999 " + delayStatistic.getP999() / 1e6);
  }

  static class DurationCalculator {

    public static DurationStatistic compute(List<Long> durations) {
      long totalDuration = durations.stream().mapToLong(Long::longValue).sum();
      long p90 = durations.get((int) (durations.size() * 0.9));
      long p99 = durations.get((int) (durations.size() * 0.99));
      long p999 = durations.get((int) (durations.size() * 0.999));

      return new DurationStatistic(totalDuration, p90, p99, p999);
    }
  }

  static class DurationStatistic {

    private long totalDuration;
    private long p90;
    private long p99;
    private long p999;

    public DurationStatistic(long totalDuration, long p90, long p99, long p999) {
      this.totalDuration = totalDuration;
      this.p90 = p90;
      this.p99 = p99;
      this.p999 = p999;
    }

    public long getTotalDuration() {
      return totalDuration;
    }

    public long getP90() {
      return p90;
    }

    public long getP99() {
      return p99;
    }

    public long getP999() {
      return p999;
    }
  }
}
