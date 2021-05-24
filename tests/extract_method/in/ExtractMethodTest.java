public class ExtractMethod {

    String name = "Ali";

    void printBanner() {
        System.out.println("ExtractMethod.printBanner()");
    }

    int getOutstanding(){
        return 334;
    }

    void printOwing() {
        printBanner();

        // Print details.
        System.out.println("name: " + this.name);
        System.out.println("amount: " + getOutstanding());
    }
}