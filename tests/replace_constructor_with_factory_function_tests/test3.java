public class Employee {
  int modelYear;
  String modelName;

  public Employee(int year, String name) {
    modelYear = year;
    modelName = name;
  }

  public static void main(String[] args) {
    Main myCar = new Employee(1969, "Mustang");
    System.out.println(myCar.modelYear + " " + myCar.modelName);

    int x = 5;
    int y = 6;
    int sum = x + y;
  }
}
