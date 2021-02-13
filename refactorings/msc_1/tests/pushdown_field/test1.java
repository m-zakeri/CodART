package pushdown_field_test1;

public class A
{
    int a;
}

class B extends A
{
    int b, c, d;
}

class C extends A
{
    int[] b, c;

    C()
    {
        b = null;
    }

    C(int d)
    {
        c = new int[1];
    }
}
