import java.util.*;

public class StudentGrades {
    private String[] students;
    private double[] grades;
    private int studentCount;

    public StudentGrades(int capacity) {
        students = new String[capacity];
        grades = new double[capacity];
        studentCount = 0;
    }

    public void addStudent(String studentName, double grade) {
        if (studentCount < students.length) {
            students[studentCount] = studentName;
            grades[studentCount] = grade;
            studentCount++;
            System.out.println("Student added: " + studentName + " with grade " + grade);
        } else {
            System.out.println("Cannot add more students. List is full.");
        }
    }

    public void removeStudent(String studentName) {
        boolean found = false;
        for (int i = 0; i < studentCount; i++) {
            if (students[i].equals(studentName)) {
                for (int j = i; j < studentCount - 1; j++) {
                    students[j] = students[j + 1];
                    grades[j] = grades[j + 1];
                }
                students[studentCount - 1] = null;
                grades[studentCount - 1] = 0;
                studentCount--;
                found = true;
                System.out.println("Student removed: " + studentName);
                break;
            }
        }
        if (!found) {
            System.out.println("Student not found.");
        }
    }

    public void displayGrades() {
        if (studentCount == 0) {
            System.out.println("No students available.");
        } else {
            System.out.println("Student Grades:");
            for (int i = 0; i < studentCount; i++) {
                System.out.println(students[i] + ": " + grades[i]);
            }
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        StudentGrades gradesSystem = new StudentGrades(5); // Max 5 students

        while (true) {
            System.out.println("1. Add Student");
            System.out.println("2. Remove Student");
            System.out.println("3. Display Grades");
            System.out.println("4. Exit");
            System.out.print("Choose an option: ");
            int choice = scanner.nextInt();
            scanner.nextLine();  // Consume newline

            switch (choice) {
                case 1:
                    System.out.print("Enter student name: ");
                    String studentName = scanner.nextLine();
                    System.out.print("Enter student grade: ");
                    double grade = scanner.nextDouble();
                    gradesSystem.addStudent(studentName, grade);
                    break;
                case 2:
                    System.out.print("Enter student name to remove: ");
                    studentName = scanner.nextLine();
                    gradesSystem.removeStudent(studentName);
                    break;
                case 3:
                    gradesSystem.displayGrades();
                    break;
                case 4:
                    System.out.println("Exiting system.");
                    return;
                default:
                    System.out.println("Invalid choice.");
            }
        }
    }
}
