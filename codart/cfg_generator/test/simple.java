public class SimpleProgram {
    public static void main(String[] args) {
        String name = "User";
        int age = 30;

        String greeting = "Hello, " + name + "!";
        String ageMessage = "Your age is: " + age;

        int doubleAge = age * 2;
        String doubleAgeMessage = "Twice your age is: " + doubleAge;

        String farewell = "Have a great day!";

        System.out.println(greeting);
        System.out.println(ageMessage);
        System.out.println(doubleAgeMessage);
        System.out.println(farewell);
    }
}
