public class Car{
    private Engine engine = new Engine();
    

    public static void main(String args[]){
     String model = "Hello Java";
     
     System.out.println(model);
    }

    public void Run(String args[]){
     String text = "Hello Java";
     
     System.out.println(text);
    }
    
    public void Drive(String args, ){
        this.engine.SetName("Yamaha", "last");
    }
}



class Engine{
    public String Name;
    

    public static void main(String args[], ){
     String text = "Hello Java";
     System.out.println(text);
    }
    public void SetName(String X, ){
        
        this.Name = X;
    }
    

}