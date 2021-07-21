//Java program to overload constructors
class Employee{
    int id;
    String name;
    int age;
    //creating two arg constructor
    private Employee(int i,String n){
    id = i;
    name = n;
    }
    public static Employee Create( int i, String n){
       return new Employee(i, n)}
    //creating three arg constructor
    private Employee(int i,String n,int a){
    id = i;
    name = n;
    age=a;
    }
    public static Employee Create( int i, String n, int a){
       return new Employee(i, n, a)}

    void display(){System.out.println(id+" "+name+" "+age);}
    public static void main(String args[]){
    Employee s1 = Employee.Create(111,"Karan");
    Employee s2 = Employee.Create(222,"Aryan",25);
    s1.display();
    s2.display();
   }
}