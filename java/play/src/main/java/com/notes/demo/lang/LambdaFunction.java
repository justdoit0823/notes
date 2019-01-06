package com.notes.demo.lang;

public class LambdaFunction {

  public static void main(String[] args) {

    int a = 1;
    int b = 2;
    Operator sum = (x, y) -> x + y;
    int c = sum.intSum(a, b);

    System.out.printf("%d + %d = %d.\n", a, b, c);
  }

  interface Operator {
    int intSum(int x, int y);
  }
}
