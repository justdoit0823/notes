package com.notes.demo.lang;

import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.IOException;

public class ParseJson {

  private static final String TEST_JSON = "{\"x\": 123, \"y\": \"haha\"}";

  public static void main(String[] args) {
    try {
      ObjectMapper mapper = new ObjectMapper();
      System.out.println(mapper.readValue(TEST_JSON, Foo.class));
    } catch (IOException e) {
      System.out.println(e);
    }
  }

  static class Foo {

    private int x;
    private String y;

    public int getX() {
      return x;
    }

    public void setX(int x) {
      this.x = x;
    }

    public String getY() {
      return y;
    }

    public void setY(String y) {
      this.y = y;
    }

    @Override
    public String toString() {
      return "Foo{" + "x=" + x + ", y='" + y + '\'' + '}';
    }
  }
}
