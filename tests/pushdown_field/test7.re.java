package pushdown_field_test3;

class ClassWith_a
{
    int a;
}

class B
{
    ClassWith_a var1 = 0;
    void a()
    {
        var1.a = 4;
        b.a = 0;
        pushdown_field_test1.A var1;
        c.a = 0;
        d.a = c.a;
        //var1.a = 2; // Fails
    }
}

class C
{
    pushdown_field_test1.A a;
    void b()
    {
        c.a = 0;
    }
}
