public class Employee {
  int modelYear;
  String modelName;

  private Employee(int year, String name) {
    modelYear = year;
    modelName = name;
  }
    public static Employee Create( int year, String name){
       return new Employee(year, name)}

  public static void main(String[] args) {
    Main myCar = Employee.Create(1969,"Mustang");
    System.out.println(myCar.modelYear + " " + myCar.modelName);

    int x = 5;
    int y = 6;
    int sum = x + y;
  }
}
