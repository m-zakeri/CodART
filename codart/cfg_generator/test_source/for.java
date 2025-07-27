// public class SimpleLoopExample {
//     public static void main(String[] args) {
//         // Initialize variables
//         int sum = 0;
//         int count = 1;
//
//         // Start a for loop
//         for (int i = 1; i <= 10; i++) {
//             // Add current value to sum
//             sum += i;
//
//             // Print current value
//             System.out.println("Number " + i);
//         }
//
//         // Print final sum after loop
//         System.out.println("Sum of numbers: " + sum);
//     }
// }
public class Instances
{
    public int DeleteParent(int nParent)
    {
        // Validate input parameters
        if (nParent < 0 || nParent >= _instances.Count)
        {
            throw new ArgumentOutOfRangeException(nameof(nParent), "Invalid index");
        }



        // Perform the deletion operation
        var parent = _instances[nParent];

        // Remove the parent from the list
        _instances.RemoveAt(nParent);

        return nParent; // Return the index of the deleted parent
    }
}

