public class Car{
    private Engine engine = new Engine();
    

    public static void main(String args[]){
     String model = "Hello Java";
     String dead = "dead";
     System.out.println(model);
    }

    public void Run(String args[]){
     String text = "Hello Java";
     int number = 5 + 10;
     System.out.println(text);
    }
    
    public void Drive(String args, int wheels){
        this.engine.SetName("Yamaha", "last");
    }
}



class Engine{
    public String Name;
    

    public static void main(String args[], int k){
     String text = "Hello Java";
     System.out.println(text);
    }
    public void SetName(String X, String last){
        Car what = new Car();
        this.Name = X;
    }
    

}