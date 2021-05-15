import targetPackage.Source;

public class Test {

  public void test_main() {
    System.out.println("hello main method");    
  }

  public void method1() {
    Source source = new Source();
    source.method2();
  }
}

