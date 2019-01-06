package com.notes.demo.lang;

import java.lang.Thread;

class HelloWorldThread extends Thread {

  public void run() {

    System.out.println("Welcome to the hello world thread");

    try {
      Thread.sleep(2000);
    } catch (InterruptedException e) {
      System.out.println("Hello world thread was interrupted.");
    }

    System.out.println("finish execution in the hello world thread");
  }

  public static void main(String[] args) {

    HelloWorldThread thread = new HelloWorldThread();
    thread.start();
  }
}
