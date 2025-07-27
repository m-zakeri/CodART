import java.util.*;

public class TaskManager {
    private List<String> tasks;

    public TaskManager() {
        tasks = new ArrayList<>();
    }

    public void addTask(String task) {
        tasks.add(task);
    }

    public void removeTask(String task) {
        if (tasks.contains(task)) {
            tasks.remove(task);
            System.out.println("Task removed: " + task);
        } else {
            System.out.println("Task not found.");
        }
    }

    public void displayTasks() {
        if (tasks.isEmpty()) {
            System.out.println("No tasks available.");
        } else {
            System.out.println("Task List:");
            for (String task : tasks) {
                System.out.println(task);
            }
        }
    }

    public void markTaskCompleted(String task) {
        if (tasks.contains(task)) {
            tasks.remove(task);
            tasks.add(task + " (Completed)");
            System.out.println("Task marked as completed: " + task);
        } else {
            System.out.println("Task not found.");
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        TaskManager manager = new TaskManager();

        while (true) {
            System.out.println("1. Add Task");
            System.out.println("2. Remove Task");
            System.out.println("3. Display Tasks");
            System.out.println("4. Mark Task as Completed");
            System.out.println("5. Exit");
            System.out.print("Choose an option: ");
            int choice = scanner.nextInt();
            scanner.nextLine();  // Consume the newline character

            switch (choice) {
                case 1:
                    System.out.print("Enter task to add: ");
                    String task = scanner.nextLine();
                    manager.addTask(task);
                    break;
                case 2:
                    System.out.print("Enter task to remove: ");
                    task = scanner.nextLine();
                    manager.removeTask(task);
                    break;
                case 3:
                    manager.displayTasks();
                    break;
                case 4:
                    System.out.print("Enter task to mark as completed: ");
                    task = scanner.nextLine();
                    manager.markTaskCompleted(task);
                    break;
                case 5:
                    System.out.println("Exiting program.");
                    return;
                default:
                    System.out.println("Invalid choice.");
            }
        }
    }
}
