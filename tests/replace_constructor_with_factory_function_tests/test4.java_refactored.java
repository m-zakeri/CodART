class Employee {
  private Employee(int type) {
    this.type = type;
  }
    public static Employee Create( int type){
       return new Employee(type)}
  // ...
}

/*
class Employee {
  static Employee create(int type) {
    employee = new Employee(type);
    // do some heavy lifting.
    return employee;
  }
  // ...
}
*/