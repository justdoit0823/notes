package com.notes.demo.bench;

import com.google.common.cache.CacheLoader;
import com.google.common.cache.LoadingCache;
import com.google.common.cache.CacheBuilder;

import java.util.Collections;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
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

    ExecutorService executorService = Executors.newFixedThreadPool(concurrence);
    List<Integer> testSequences = IntStream.rangeClosed(1, concurrence).boxed().collect(Collectors.toList());
    List<Callable<Boolean>> tasks = Collections.emptyList();
    if (operation.equals("read")) {
      tasks = getReadTasks(uid, testSequences);
    } else if (operation.equals("write")) {
      tasks = getWriteTasks(uid, testSequences);
    }

    long startTs = System.nanoTime();
    try {
      executorService.invokeAll(tasks);
    } catch (InterruptedException e) {
      System.out.println(e);
    }
    long stopTs = System.nanoTime();

    final long duraton = (stopTs - startTs) / 1000000L;
    System.out.println(operation + " concurrence:" + concurrence + ", duration:" + duraton + ", ops:" + concurrence * 5000 / (duraton / 1000.0));
    System.exit(0);
  }

  private static List<Callable<Boolean>> getReadTasks(int uid, List<Integer> testSequences) {
    return testSequences.stream().map((i) -> (Callable<Boolean>) () -> {
      int num  = 5000;
      while (num-- > 0) {
        try {
          localCache.get(uid);
        } catch (ExecutionException e) {
          System.out.println(e);
        }
      }
      return true;
    }).collect(Collectors.toList());
  }

  private static List<Callable<Boolean>> getWriteTasks(int uid, List<Integer> testSequences) {
    return testSequences.stream().map((i) -> (Callable<Boolean>) () -> {
      int num = 50000;
      while (num-- > 0) {
        localCache.put(uid + i, 112312312);
      }
      return true;
    }).collect(Collectors.toList());
  }
}
