

class Person {

    String name;
    private int age;

    public Person(String n, int age) {
	name = n;
	this.age = age;
    }

    public String getName() {
	return name;
    }

    public int getAge() {
	return age;
    }

    public void setAge(int n) {
	age = n;
    }

}

class VariableVisibility {

    public static void main(String[] args) {
	Person p1 = new Person("Zhangsan", 20);
	System.out.println(p1.getName());

	System.out.println(p1.getAge());

	p1.setAge(22);
	System.out.println(p1.getAge());
    }

}
