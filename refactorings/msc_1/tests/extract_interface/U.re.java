package test;

class U
{
    private Iab a = A();
    private Iab b1 = B();
    private B b2 = B();

    private B c2;
    private Iab c1;

    void func1()
    {
        a.a();
        b1.a();
        b2.b();
        b2.c();

        c1.b();
        c2.c();
    }

    void func2()
    {
        B a;
        a.a();
        a.c();
        Iab b;
        b.b();
        b.a();
    }
}
