// File AnotherClass.java
public class AnotherClass {
    public void method() {
        Employee aClass = new Employee("string");
    }
}

// File Class.java
public class Employee {
    public Employee(String s) {
        super( );
        this.s = s;
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