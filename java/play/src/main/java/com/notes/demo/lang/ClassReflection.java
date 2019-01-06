package com.notes.demo.lang;

import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.lang.reflect.InvocationTargetException;

public class ClassReflection {

  public static void main(String[] args) {
    int x = 10000;
    int x2 = 1;
    int x3 = x;
    String y = "hahaha";

    double k = 9.87;
    int k1 = (int) k;

    System.out.println(x);
    x += 1;
    System.out.println(x);
    x = x + 1;
    System.out.println(x);

    Object z = new Object();
    for (int i = 0; i < 10; i++) {
      System.out.println(i);
    }
    System.out.println(ClassReflection.class);
    System.out.println(Integer.class);

    Foo testObj = new Foo(123123);
    try {
      Field fx = Foo.class.getDeclaredField("x");
      fx.setAccessible(true);
      System.out.println(fx.get(testObj));
    } catch (NoSuchFieldException | IllegalAccessException e) {
      System.out.println(e);
    }

    try {
      Method ms = Foo.class.getDeclaredMethod("showFoo");
      ms.setAccessible(true);
      System.out.println(ms.invoke(testObj));
    } catch (NoSuchMethodException | InvocationTargetException | IllegalAccessException e) {
      System.out.println(e);
    }
  }

  static class Foo {

    private Integer x;

    public Foo(Integer x) {
      this.x = x;
    }

    private String showFoo() {
      return "Foo<" + x + ">";
    }
  }
}
