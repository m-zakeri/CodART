//Java program to overload constructors
class Employee{
    int id;
    String name;
    int age;

    //creating two arg constructor
    Employee(int i,String n){
    id = i;
    name = n;
    }

    //creating three arg constructor
    Employee(int i,String n,int a){
    id = i;
    name = n;
    age=a;
    }

    void display(){System.out.println(id+" "+name+" "+age);}

    public static void main(String args[]){
    Employee s1 = new Employee(111,"Karan");
    Employee s2 = new Employee(222,"Aryan",25);

    s1.display();
    s2.display();
   }
}