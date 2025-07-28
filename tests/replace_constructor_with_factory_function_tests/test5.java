//Java program to initialize the values from one object to another object.
class Employee{
    int id;
    String name;

    //constructor to initialize integer and string
    Employee(int i,String n){
    id = i;
    name = n;
    }

    //constructor to initialize another object
    Employee(Employee s){
    id = s.id;
    name =s.name;
    }

    void display(){System.out.println(id+" "+name);}

    public static void main(String args[]){
    Employee s1 = new Employee(111,"Karan");
    Employee s2 = new Employee(222,"Aryan");
    Employee s3 = new Employee(s1);

    s1.display();
    s2.display();
    s3.display();
   }
}