public class ExtractMethodTest {

    public static void printOwing2() {
        int a;
        a = 5;
        
        int[] c = {5,6,45,65};
        String fName = "hello",lName = "world";

        int b = printDetails(a, c, fName, lName);
        System.out.println(b);
    }
    private static void printDetails(int a, int[] c, String fName, String lName);
    {
        System.out.println(a+c+fName+lName);
        int b = 12;
    	return b;
    }
}