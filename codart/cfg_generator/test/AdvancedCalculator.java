import java.util.Scanner;

public class AdvancedCalculator {

    public int add(int a, int b) {
        return a + b;
    }

    public int subtract(int a, int b) {
        return a - b;
    }

    public int multiply(int a, int b) {
        return a * b;
    }

    public int divide(int a, int b) throws ArithmeticException {
        if (b == 0) {
            throw new ArithmeticException("Cannot divide by zero");
        }
        return a / b;
    }

    public static void main(String[] args) {
        AdvancedCalculator calculator = new AdvancedCalculator();
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter first number: ");
        int num1 = scanner.nextInt();

        System.out.print("Enter second number: ");
        int num2 = scanner.nextInt();

        System.out.print("Choose operation (add, subtract, multiply, divide): ");
        String operation = scanner.next();

        try {
            int result = 0;
            switch (operation) {
                case "add":
                    result = calculator.add(num1, num2);
                    break;
                case "subtract":
                    result = calculator.subtract(num1, num2);
                    break;
                case "multiply":
                    result = calculator.multiply(num1, num2);
                    break;
                case "divide":
                    result = calculator.divide(num1, num2);
                    break;
                default:
                    System.out.println("Invalid operation");
                    System.exit(1);
            }

            System.out.println("The result is: " + result);
        } catch (ArithmeticException e) {
            System.out.println("Error: " + e.getMessage());
        }

        scanner.close();
    }
}
