public class Employee {

    private String text;

    public static void main(String[] args) {
        Employee DisplayApp = new Employee("Hello");
    }

    public Employee(String text) {
        super( );
        this.text = text;
    }
}

/*
public class Employee {

    private String text;

    public static void main(String[] args) {
        Employee DisplayApp = createDisplayApp("Hello");
    }

    public static Employee createDisplayApp(java.lang.String text) {
               return new Employee(text);
               }

    private Employee(String text) {
*/