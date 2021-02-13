package pullup_field_test1;

public class A
{
    int[] a;
    public A() {}
}

class B extends A
{
    B() { a = null; }
    int b, c, d;
}

class C extends A
{
    int[] b, c;

    C()
    {
        a = new int[] {1,2};
        b = null;
    }

    C(int d)
    {
        a = new int[] {1,2};
        c = new int[1];
    }
}
