// File Class.java
public class Employee {
    private Employee(String s, int r) {
        this.s = s;
    }
    public static Employee Create( String s, int r){
       return new Employee(s, r)}
}

// File AnotherClass.java
public class AnotherClass {
    public void method() {
        Employee aClass = Employee.Create("string");
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