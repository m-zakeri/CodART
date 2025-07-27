// public class IncrementListValues {
// private static void method(List<Integer> list){
//         int x = 10;
//         int y = 10;
//         for(Integer k :  list){
//             x++;
//             y++;
//             System.out.println(x);
//         }
//     }
//
// }
//



import java.util.Scanner;

public class QuadraticEquation {
    public static void main(String[] args) {

    Scanner scanner = new Scanner(System.in);
    System.out.print("Enter the coefficient a: ");
    double a = scanner.nextDouble();
    System.out.print("Enter the coefficient b: ");
    double b = scanner.nextDouble();
    System.out.print("Enter the coefficient c: ");
    double c = scanner.nextDouble();
    double discriminant = b * b - 4 * a * c;

    if (discriminant > 0) {
    double root1 = (-b + Math.sqrt(discriminant)) / (2 * a);
    double root2 = (-b - Math.sqrt(discriminant)) / (2 * a);
    System.out.println("The roots are real and different.");
    System.out.println("Root 1: " + root1);
    System.out.println("Root 2: " + root2);
    } else if (discriminant == 0) {
    double root = -b / (2 * a);
    System.out.println("The roots are real and the same.");
    System.out.println("Root: " + root);
    } else {
    double realPart = -b / (2 * a);
    double imaginaryPart = Math.sqrt(-discriminant) / (2 * a);
    System.out.println("The roots are complex and different.");
    System.out.println("Root 1: " + realPart + " + " + imaginaryPart + "i");
    System.out.println("Root 2: " + realPart + " - " + imaginaryPart + "i");
    }
    }
}

