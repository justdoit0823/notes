package com.notes.demo.lang;

import java.util.HashMap;
import java.util.Map;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;

public class RetrieveAnnotation {

  public static void main(String[] args) {
    Request request = new Request();
    Map<String, String> data = new HashMap<>();

    try {
      data.put("A", "1");
      assert !request.process("/", "GET", data);
      assert !request.process("/", "POST", data);

      data.put("B", "2");
      data.put("C", "3");
      assert !request.process("/", "GET", data);
      assert request.process("/", "POST", data);
    } catch (NoSuchMethodException e) {
      System.out.println(e);
    }

    System.out.println("done");
  }

  static class Request {

    @MethodAnnotation(
        method = "POST",
        requiredFields = {"A", "B", "C"})
    private boolean process(String path, String method, Map<String, String> data)
        throws NoSuchMethodException {
      MethodAnnotation annotation =
          Request.class
              .getDeclaredMethod("process", String.class, String.class, Map.class)
              .getAnnotation(MethodAnnotation.class);

      if (!method.equals(annotation.method())) return false;

      for (String f : annotation.requiredFields()) {
        if (data.get(f) == null) return false;
      }

      return true;
    }

    @Retention(RetentionPolicy.RUNTIME)
    public @interface MethodAnnotation {

      String method() default "GET";

      String[] requiredFields();
    }
  }
}
