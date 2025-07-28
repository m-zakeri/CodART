package com.company;

public class Main {

    public static void main(String[] args) {
        Student reza = new Student("97524698", "reza", 20);
        reza.actionNumberOne();
        reza.actionNumberTwo();
    }

}


class Student {
    private String studentId;
    private String name;
    private int age;

    public Student(String studentId, String name, int age) {
        this.studentId = studentId;
        this.name = name;
        this.age = age;
    }

    public void actionNumberOne() {
        this.name = "IUST_" + this.name;
        printStudent("1 ", "Student details ");
    }

    public void actionNumberTwo() {
        this.age = 32;
        printStudent("2 ", "Student information ");
    }


    public String getStudentId() {
        return studentId;
    }

    public void setStudentId(String studentId) {
        this.studentId = studentId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

	public void printStudent(String variable59Number01, String variable59Number11) {
		System.out.print(variable59Number01);
		System.out.print(variable59Number11);
		System.out.print("Student { ");
		System.out.print("name: "+this.name+", ");
		System.out.print("age: "+this.age+", ");
		System.out.print("studentId: "+this.studentId+" }\n");
	}

}

