package pullup_field_test5;

public class A
{
    int id;
    public A() {}
}

class B extends A
{
    
    int a[] = null, b, c, d;
}

class C extends B
{
    int[] b, a = { 1, 2 }, c;
    
    
    C()
    {
        b = null;
    }

    C(int d)
    {
        System.out.println(this.id);
        id = d;
    }
}

class D extends A{
    

    D(int d)
    {
        id = d;
    }
}