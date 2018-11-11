package com.notes.demo.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/version/")
public class Version {

    @GetMapping("/")
    public String version() {
        System.out.println("call version.");
        return "0.1";
    }
}
