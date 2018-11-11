package com.notes.demo.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.LinkedList;
import java.util.Random;

@RestController
@RequestMapping("/api/v1/sort/")
public class SortComparison {

    private static Random rand = new Random();

    public String sort(@PathVariable("start") int start, @PathVariable("stop") int stop, @PathVariable("num") int num) {
        List<Integer> samples = new LinkedList<>();
        for (int i = 0; i < num; i++) {
            samples.add(rand.nextInt(stop - start) + start);
        }

        samples.sort(null);

        return "done";
    }
}
