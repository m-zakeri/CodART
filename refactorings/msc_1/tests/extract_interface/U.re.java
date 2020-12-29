package test;

class U
{
    A a = A();
    B b1 = B();
    B b2 = B();

    void func1()
    {
        a.a();
        b1.a();
        b2.b();
        b2.c();
    }

    void func2()
    {
        B a;
        a.a();
        a.c();
    }
}
