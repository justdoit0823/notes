package com.notes.demo;

import com.notes.demo.bench.CascadeThreadPoolBench;
import com.notes.demo.bench.GuavaLoadingCacheBench;
import com.notes.demo.bench.QueueDelayBench;
import java.util.Arrays;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class DemoApplication {

  public static void main(String[] args) {
    SpringApplication.run(DemoApplication.class, args);

    String[] i = new String[args.length - 1];
    String command = args[0];
    String[] testArgs = Arrays.asList(args).subList(1, args.length).toArray(i);
    if (command.equals("GuavaLoadingCacheBench")) {
      GuavaLoadingCacheBench.main(testArgs);
    } else if (command.equals("QueueDelayBench")) {
      QueueDelayBench.main(testArgs);
    } else if (command.equals("CascadeThreadPoolBench")) {
      CascadeThreadPoolBench.main(testArgs);
    }
  }
}
