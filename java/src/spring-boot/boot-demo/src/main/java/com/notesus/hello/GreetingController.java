package com.notesus.hello;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.notesus.service.CacheService;
import com.notesus.service.RedisService;

import java.io.IOException;
import java.util.concurrent.atomic.AtomicLong;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import com.fasterxml.jackson.databind.ObjectMapper;

import javax.annotation.Resource;

@RestController
public class GreetingController {

    private static final String template = "Hello, %s!";
    private final AtomicLong counter = new AtomicLong();

    @Autowired
    private CacheService redisService;

    @RequestMapping("/greeting")
    public Greeting greeting(@RequestParam(value="name", defaultValue="World") String name) {
        final long count = counter.incrementAndGet();
        redisService.set(name, String.valueOf(count));

        ObjectMapper objectMapper=new ObjectMapper();
        Dataset d1 = new Dataset(1231, 123L);
        Dataset d2 = null;
        try {
            System.out.println(objectMapper.writeValueAsString(d1));
            d2 = objectMapper.readValue("{\"readDuration\": 1, \"ts\": 123}", Dataset.class);
        } catch (JsonProcessingException e) {
            System.out.println(e);
        } catch (IOException e) {
            System.out.println(e);
        }

        if (d2 != null) {
            System.out.println(d2.getReadDuration());
        }

        System.out.println(DataType.IMAGE);

        System.out.println("greeting controller done...");
        return new Greeting(count, String.format(template, name));
    }

    static class Dataset {
        private int readDuration;
        private long ts;

        public Dataset() {

        }

        public Dataset(int readDuration, long ts) {
            this.readDuration = readDuration;
            this.ts = ts;
        }

        public int getReadDuration() {
            return readDuration;
        }

        public void setReadDuration(int readDuration) {
            this.readDuration = readDuration;
        }

        public long getTs() {
            return ts;
        }

        public void setTs(long ts) {
            this.ts = ts;
        }
    }

    static  enum DataType {
        TEXT(1),
        IMAGE(2);

        private int value;

        DataType(int v) {
            value = v;
        }

    }
}
