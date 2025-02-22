

interface MyStrategy {
	public int doOperation(int num1, int num2);
}
class SubNewClass1 implements MyStrategy{
	@Override
	public int doOperation(int num1, int num2)
	{
            return num1 + num2;
        }
}
class SubNewClass2 implements MyStrategy{
	@Override
	public int doOperation(int num1, int num2)
	{
            return num1 - num2;
        }
}
class SubNewClass3 implements MyStrategy{
	@Override
	public int doOperation(int num1, int num2)
	{
            return num1 * num2;
        }
}
class Context
{
    private MyStrategy strategy;
	public Context(MyStrategy strategy){
		this.strategy = strategy;
	}
	public int executeStrategy(int num1, int num2){
		return strategy.doOperation( num1,  num2);
	}
}
public class Main {
   public static void main(String[] args) {
      Context context = new Context();
      System.out.println("10 + 5 = " + context.execute(10,5,'+'));
      System.out.println("10 - 5 = " + context.execute(10,5,'-'));
      System.out.println("10 * 5 = " + context.execute(10,5,'*'));
    }
}