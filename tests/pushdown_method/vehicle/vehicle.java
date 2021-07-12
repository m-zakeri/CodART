package pushdown_method_test_vehicle;

class Vehicle {
    protected String brand;
    protected string id;

  private void getId() {
    System.out.println(id);
  }

  protected void getId2() {
    System.out.println(id);
  }

  protected String owner = "Ali"; 
  public void setBrand() {
    this.brand = "fiat";
  }    
  
public void epicMethod(){
    System.out.println("hmmmm");
  }

  public void doNothing() {
    System.out.println("doing nothing");
  }

  public void honk() {                   
    System.out.println("Tuut, tuut!");
    this.setBrand();
  }
}

class FourWheel extends Vehicle{

  protected string color;
  protected int weight = 30;
  
  public void doNothing() {
    epicMethod();
    System.out.println("doing something");
  }

  public void printName(){
    System.out.println("four wheel");
  }
}

class Car extends FourWheel {
    Car() { color = "red"; }
    
     
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

class bicycle extends Vehicle {
    private String modelName = "Mustang";    // Car attribute
    private String owner = "shams";
    protected string color = "red";
  public static void main(String[] args) {

    // Create a myCar object
    bicycle myCar = new bicycle();

    // Call the honk() method (from the Vehicle class) on the myCar object
    myCar.honk();

    // Display the value of the brand attribute (from the Vehicle class) and the value of bicycle modelName from the bicycle class
    System.out.println(myCar.brand + " " + myCar.modelName);
  }

}
