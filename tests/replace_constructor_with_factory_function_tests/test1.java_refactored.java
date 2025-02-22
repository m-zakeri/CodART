 class Employee {
    private int _type;
    static final int ENGINEER = 0;
    static final int SALESMAN = 1;
    static final int MANAGER = 2;247
    private Employee (int type, String name) {
        _type = type;
    }
    public static Employee Create( int type, String name){
       return new Employee(type, name)}
 }

 public class main {
    Employee eng = Employee.Create(Employee.ENGINEER,"Name");
}
/*
  class Employee {
    private int type;
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