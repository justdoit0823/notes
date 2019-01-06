package com.notes.demo.lang;

public class NullObjectMethodInvoke {

  public static void main(String[] args) {
    Resolver r1 = null;
    r1.showName();
  }

  class Resolver {

    public void showName() {
      System.out.println("Resolver...");
    }
  }
}
