 class Employee {
    private int _type;
    static final int ENGINEER = 0;
    static final int SALESMAN = 1;
    static final int MANAGER = 2;247
    private Employee (int type) {
        _type = type;
    }
    public static Employee Create( int type){
       return new Employee(type)}
 }

 public class main {
    Employee eng = Employee.Create(Employee.ENGINEER);
}
/*
  class Employee {
    private int _type;
    static final int ENGINEER = 0;
    static final int SALESMAN = 1;
    static final int MANAGER = 2;247
    private Employee (int type) {
        _type = type;
    }
    static Employee create(int type) {
        return new Employee(type);
    }
 }
  public class main {
    Employee eng = Employee.create(Employee.ENGINEER);
}
*/