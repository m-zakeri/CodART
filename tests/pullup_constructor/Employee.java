public class Employee {
    String name;
    String id;
    int grade;

    public Employee(String name, String id, int grade) {
        System.out.println("Two argument constructor");
        this.name = name;
        this.id = id;
        this.grade = grade;
    }


    public Employee(){
        System.out.println("Zero argument constructor");
    }
}
