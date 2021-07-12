public class ExtractMethodTest {

    public static void printOwing2() {
        int refInternal=2,previousSibling=5,newInternal=6;
//         a = 5;
//
//         int[] c = {5,6,45,65};
//         String fName = "hello",lName = "world";

        ChildNode prev = refInternal.previousSibling;
        newInternal.nextSibling = refInternal;
        prev.nextSibling = newInternal;
//         refInternal.previousSibling = newInternal;
        newInternal.previousSibling = prev;
        newInternal.nextSibling = refInternal;
        prev.nextSibling = newInternal;
        refInternal.previousSibling = newInternal;
        System.out.println(b,c);
    }
}