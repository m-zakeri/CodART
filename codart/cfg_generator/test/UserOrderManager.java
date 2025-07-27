import java.util.*;

public class UserOrderManager {
    public static void main(String[] args) {
        List<User> users = new ArrayList<>();

        // Initialize users with nested orders
        for (int i = 0; i < 3; i++) {
            User user = new User("User" + i, new ArrayList<>());
            for (int j = 0; j < 2; j++) {
                Order order = new Order("Order" + j, new ArrayList<>());
                for (int k = 0; k < 3; k++) {
                    order.addItem("Item" + k + "-User" + i);
                }
                user.addOrder(order);
            }
            users.add(user);
        }

        // Process orders and calculate total items
        int totalItems = 0;
        for (User user : users) {
            for (Order order : user.getOrders()) {
                totalItems += order.getItems().size();
                System.out.println("Processing " + user.getName() + " -> " + order.getName() + " : " + order.getItems());
            }
        }
        System.out.println("Total items processed: " + totalItems);
    }
}