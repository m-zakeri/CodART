public class ExtractMethodTest {

    public static void printOwing2() {
        printBanner();
        String fname = "hello",lname = "world";

		printDetails(fname, lname);
    }
	private void printDetails(String fname, String lname)
	{
        System.out.println("fname: " + fname+", lname"+lname);
        System.out.println("name printed ");
	}
}