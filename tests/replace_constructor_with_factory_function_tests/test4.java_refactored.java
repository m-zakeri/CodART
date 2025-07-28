class OuterClass {
  int x = 10;

  class Employee {
    int y ;

    private Employee(){
    y = 2+100;
    }
    public static Employee Create( ){
       return new Employee()}
    public int myInnerMethod() {
      return x;
    }
  }
}

public class Main {
  public static void main(String[] args) {
    OuterClass myOuter = new OuterClass();
    OuterClass.Employee myInner = Employee.Create();
    System.out.println(myInner.myInnerMethod());
  }
}