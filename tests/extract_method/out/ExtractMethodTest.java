package example;
public class ExtractMethodTest{
    public void main(int x, long y) {
        int z = 0;
        long k = 1;
		print(y);
        int f = 0;
        for (int x = 0;x<5;x++)
        {
            System.out.println("amount: "+z);
            System.out.println("name: "+ f );
        }
    }
	public void print(long y)
	{
        System.out.println("name: "+ y );
        int f = 0;
        System.out.println("name: "+ f );
	}
}
