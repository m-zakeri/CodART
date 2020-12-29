package test;

class U
{
    private A a = A();
    private B b1 = B();
    private B b2 = B();

    private B c1, c2;

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
        A b;
        b.b();
        b.a();
    }
}
