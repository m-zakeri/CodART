class SC
{
    public void m1()
    {
        System.out.println("m1");
    }
    public void m2()
    {
        System.out.println("m2");
    }
    public void m3()
    {
        System.out.println("m3");
    }
}
class CC1 extends SC
{
    void m4()
    {
        System.out.println("m4");
    }
}
class CC2 extends SC
{
    void m5()
    {
        System.out.println("m5");
    }
}
class CC3 extends SC
{
    void m6()
    {
        System.out.println("m6");
    }
}
public class Main
{
    public static void main(String[] args)
    {
        CC1 obj1 = new CC1();
        CC2 obj2 = new CC2();
        CC3 obj3 = new CC3();
        obj1.m1();
        obj1.m4();
        obj2.m2();
        obj2.m5();
        obj3.m3();
        obj3.m6();
    }
}