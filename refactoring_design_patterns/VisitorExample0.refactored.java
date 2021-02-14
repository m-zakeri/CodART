
interface VisitorSC
{
	public void visit(CC1 m1);
	public void visit(CC2 m2);
	public void visit(CC3 m3);
}

interface SC
{
	public void accept (VisitorSC visitor);
}

class DoVisitorSC implements VisitorSC
{
	@Override
	public void visit(CC1 m1)
	{
	System.out.println("m1");
	}
	@Override
	public void visit(CC2 m2)
	{
	System.out.println("m2");
	}
	@Override
	public void visit(CC3 m3)
	{
	System.out.println("m3");
	}
}
class CC1 implements SC
{
	@Override
	public void accept(VisitorSC visitor)
	{
		visitor.visit(this);
	}
    void m4()
    {
        System.out.println("m4");
    }
}
class CC2 implements SC
{
	@Override
	public void accept(VisitorSC visitor)
	{
		visitor.visit(this);
	}
    void m5()
    {
        System.out.println("m5");
    }
}
class CC3 implements SC
{
	@Override
	public void accept(VisitorSC visitor)
	{
		visitor.visit(this);
	}
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
        obj1.accept(new DoVisitorSC());
        obj1.m4();
        obj2.accept(new DoVisitorSC());
        obj2.m5();
        obj3.accept(new DoVisitorSC());
        obj3.m6();
    }
}