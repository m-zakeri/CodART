public class GodClass {
	private static String NAME = "NAME";
	int field1;
	int field2;
	int field3;

	public int method1() {
		return this.field1 + this.field2;
	}

	public int method2() {
		return this.field3;
	}

	public int method3() {
		return this.field2;
	}

	public void printOwing() {
		printBanner();

		// Print details.
		System.out.println("name: " + NAME);
		System.out.println("amount: " + getOutstanding());
	}

	private String getOutstanding() {
		return "123";
	}

	private void printBanner() {
		System.out.println("BANNER");
	}
}
