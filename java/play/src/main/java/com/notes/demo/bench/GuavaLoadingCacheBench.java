package com.notes.demo.bench;

import com.google.common.cache.CacheLoader;
import com.google.common.cache.LoadingCache;
import com.google.common.cache.CacheBuilder;

import com.notes.demo.task.SimpleTaskResult;
import com.notes.demo.task.TaskResult;
import com.notes.demo.task.TaskRunner;
import java.util.Collections;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.TimeUnit;
import java.util.List;

import java.util.stream.IntStream;
import java.util.stream.Collectors;

public class GuavaLoadingCacheBench {

  private static final LoadingCache<Integer, Integer> localCache = CacheBuilder.newBuilder()
      .maximumSize(1000)
      .expireAfterWrite(300, TimeUnit.SECONDS)
      .refreshAfterWrite(10, TimeUnit.SECONDS)
      .build(new CacheLoader<Integer, Integer>(){

        @Override
        public Integer load(Integer uid) throws Exception {
          Thread.sleep(3 + ThreadLocalRandom.current().nextInt(5));
          return 1;
        }

      });

  public static void main(String[] args) {

    final int uid = 123213123;
    final int concurrence = Integer.parseInt(args[0]);
    final String operation = args[1];

    List<Callable<TaskResult<Boolean>>> tasks = Collections.emptyList();
    if (operation.equals("read")) {
      tasks = getReadTasks(uid, concurrence);
    } else if (operation.equals("write")) {
      tasks = getWriteTasks(uid, concurrence);
    }

    TaskRunner<Boolean> taskRunner = new TaskRunner<>(tasks, concurrence);
    taskRunner.run();

    System.exit(0);
  }

  private static List<Callable<TaskResult<Boolean>>> getReadTasks(int uid, int taskNum) {
    return IntStream.range(0, taskNum).boxed().map((i) -> (Callable<TaskResult<Boolean>>) () -> {
      int num  = 5000;
      long startTs = System.nanoTime();
      while (num-- > 0) {
        try {
          localCache.get(uid);
        } catch (ExecutionException e) {
          System.out.println(e);
        }
      }

      long stopTs = System.nanoTime();
      return new SimpleTaskResult<>(true, (stopTs - startTs));
    }).collect(Collectors.toList());
  }

  private static List<Callable<TaskResult<Boolean>>> getWriteTasks(int uid, int taskNum) {
    return IntStream.range(0, taskNum).boxed().map((i) -> (Callable<TaskResult<Boolean>>) () -> {
      int num = 50000;
      long startTs = System.nanoTime();
      while (num-- > 0) {
        localCache.put(uid + i, 112312312);
      }

      long stopTs = System.nanoTime();
      return new SimpleTaskResult<>(true, (stopTs - startTs));
    }).collect(Collectors.toList());
  }
}
