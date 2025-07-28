//Java program to initialize the values from one object to another object.
class Employee{
    int id;
    String name;
    //constructor to initialize integer and string
    private Employee(int i,String n){
    id = i;
    name = n;
    }
    public static Employee Create( int i, String n){
       return new Employee(i, n)}

    //constructor to initialize another object
    private Employee(Employee s){
    id = s.id;
    name =s.name;
    }
    public static Employee Create( Employee s){
       return new Employee(s)}
    void display(){System.out.println(id+" "+name);}

    public static void main(String args[]){
    Employee s1 = Employee.Create(111,"Karan");
    Employee s2 = Employee.Create(222,"Aryan");
    Employee s3 = Employee.Create(s1);
    s1.display();
    s2.display();
    s3.display();
   }
}