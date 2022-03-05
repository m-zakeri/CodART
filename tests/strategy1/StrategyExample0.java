class Context
{
   public int execute(int num1, int num2, char op)
   {
        if (op == '+')
        {
            return num1 + num2;
        }
        else if (op == '-')
        {
            return num1 - num2;
        }
        else if (op == '*')
        {
            return num1 * num2;
        }
        else
            return 0;
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