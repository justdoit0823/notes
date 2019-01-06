package com.notes.demo.lang;

import java.util.Arrays;

public class PolymorphismClass {

  public static void main(String[] args) {

    Person[] totalPeople = new Person[4];

    totalPeople[0] = new Person("A", 12);
    totalPeople[1] = new Student("B", 20);
    totalPeople[2] = new Engineer("C", 32);
    totalPeople[3] = new Player("D", 27);

    Arrays.asList(totalPeople)
        .forEach(
            person -> {
              System.out.println(person.getDescription());
            });
  }

  static class Person {
    protected String name;
    private int age;

    public Person(String n, int age) {
      name = n;
      this.age = age;
    }

    public String getDescription() {
      return "I'm a person named " + name;
    }
  }

  static class Student extends Person {

    public Student(String n, int age) {
      super(n, age);
    }

    public String getDescription() {
      return "I'm a student named " + name;
    }
  }

  static class Engineer extends Person {

    public Engineer(String n, int age) {
      super(n, age);
    }

    public String getDescription() {
      return "I'm an engineer named " + name;
    }
  }

  static class Player extends Person {

    public Player(String n, int age) {
      super(n, age);
    }
  }
}
