package pushdown_field_test_vehicle;
class Vehicle {
  protected String brand = "Ford";  
  protected String owner = "Ali";      // Vehicle attribute
  public void honk() {                    // Vehicle method
    System.out.println("Tuut, tuut!");
  }
}

class Car extends Vehicle {
  private String modelName = "Mustang";    // Car attribute
  public static void main(String[] args) {

    // Create a myCar object
    Car myCar = new Car();

    // Call the honk() method (from the Vehicle class) on the myCar object
    myCar.honk();

    // Display the value of the brand attribute (from the Vehicle class) and the value of the modelName from the Car class
    System.out.println(myCar.brand + myCar.owner + " " + myCar.modelName);
  }

}

class Truck extends Vehicle {
    private String modelName = "Mustang";    // Car attribute
    private String owner = "shams";
  public static void main(String[] args) {

    // Create a myCar object
    Truck myCar = new Truck();

    // Call the honk() method (from the Vehicle class) on the myCar object
    myCar.honk();

    // Display the value of the brand attribute (from the Vehicle class) and the value of Truck modelName from the Truck class
    System.out.println(myCar.brand + " " + myCar.modelName);
  }

}