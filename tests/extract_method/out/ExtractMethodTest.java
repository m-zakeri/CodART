public class ExtractMethodTest {

    void printOwing() {
    printBanner();

    // Print details.
		printDetails();
    }
	public void printDetails()
	{
        System.out.println("name: " + name);
        System.out.println("name printed ");
	}
}