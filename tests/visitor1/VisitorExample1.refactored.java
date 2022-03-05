//ComputerPart.java
interface VisitorComputerPart
{
	public void visit(Keyboard DisplayingKeyboard);
	public void visit(Monitor DisplayingMonitor);
	public void visit(Mouse DisplayingMouse);
	public void visit(Computer DisplayingComputer);
}
interface ComputerPart
{
	public void accept (VisitorComputerPart visitor);
}
class DoVisitorComputerPart implements VisitorComputerPart
{
	@Override
	public void visit(Keyboard DisplayingKeyboard)
	{
	System.out.println("Displaying Keyboard.");
	}
	@Override
	public void visit(Monitor DisplayingMonitor)
	{
	System.out.println("Displaying Monitor.");
	}
	@Override
	public void visit(Mouse DisplayingMouse)
	{
	System.out.println("Displaying Mouse.");
	}
	@Override
	public void visit(Computer DisplayingComputer)
	{
	System.out.println("Displaying Computer.");
	}
}
//Keyboard.java
class Keyboard implements ComputerPart {
	@Override
	public void accept(VisitorComputerPart visitor)
	{
		visitor.visit(this);
	}
}
//Monitor.java
class Monitor implements ComputerPart {
	@Override
	public void accept(VisitorComputerPart visitor)
	{
		visitor.visit(this);
	}
}
//Mouse.java
class Mouse implements ComputerPart {
	@Override
	public void accept(VisitorComputerPart visitor)
	{
		visitor.visit(this);
	}
}
//Computer.java
class Computer implements ComputerPart {
	@Override
	public void accept(VisitorComputerPart visitor)
	{
		visitor.visit(this);
	}
}
//VisitorPatternDemo.java
//main
public class Main {
   public static void main(String[] args) {
     Keyboard obj1 = new Keyboard();
     Monitor obj2 = new Monitor();
     Mouse obj3 = new Mouse();
     Computer obj4 = new Computer();
     obj1.accept(new DoVisitorComputerPart());
     obj2.accept(new DoVisitorComputerPart());
     obj3.accept(new DoVisitorComputerPart());
     obj4.accept(new DoVisitorComputerPart());
    }
}

