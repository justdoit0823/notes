package com.notes.demo.bench;

import com.google.common.cache.CacheBuilder;
import com.google.common.cache.CacheLoader;
import com.google.common.cache.LoadingCache;

import java.util.Scanner;
import java.util.stream.IntStream;

public class GuavaCacheFootprintBench {

  public static void main(String[] args) {
    LoadingCache<Integer, CodeObject> loadingCache = CacheBuilder.newBuilder()
        .build(new CacheLoader<Integer, CodeObject>() {
          @Override
          public CodeObject load(Integer id) throws Exception {
            return new CodeObject(id, "hahaahahahahahha");
          }
        });

    IntStream.range(0, 100000).forEach(id -> {
      try {
        loadingCache.get(id);
      } catch (Exception ignore) {

      }
    });

    System.out.println("Footprint bench done and press any key to finish.");
    Scanner sc = new Scanner(System.in);
    sc.nextInt();
  }

  private static final class CodeObject {
    private int id;
    private String code;

    public CodeObject(int id, String code) {
      this.id = id;
      this.code = code;
    }
  }
}
