package pullup_field_test1;

class A
{
    public A() {}
}

class B extends A
{
    int a[] = null, b, c, d;
}

class C extends A
{
    int[] b, a = { 1, 2 }, c;

    C()
    {
        b = null;
    }

    C(int d)
    {
        c = new int[1];
    }
}
