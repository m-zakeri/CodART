// File Class.java
public class Employee {
    public Employee(String s, int r) {
        this.s = s;
    }
}

// File AnotherClass.java
public class AnotherClass {
    public void method() {
        Employee aClass = new Employee("string");
    }
}


/*
public class Employee {
    private Employee(String s) {
         this.s = s;
    }
    public static Employee createClass(String s) {
        return new Employee(s);
    }
}
public class AnotherClass {
    public void method() {
        Employee aClass = Employee.createClass("string");
    }
}
*/