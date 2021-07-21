class OuterClass {
  int x = 10;

  class Employee {
    int y ;

    Employee(){
    y = 2+100;
    }
    public int myInnerMethod() {
      return x;
    }
  }
}

public class Main {
  public static void main(String[] args) {
    OuterClass myOuter = new OuterClass();
    OuterClass.Employee myInner = new Employee();
    System.out.println(myInner.myInnerMethod());
  }
}