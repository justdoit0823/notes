package com.notesus.bootdemo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class BootDemoApplication {

	public static void main1(String[] args) {
		System.out.println("start boot demo application");
		SpringApplication.run(BootDemoApplication.class, args);
	}
}
