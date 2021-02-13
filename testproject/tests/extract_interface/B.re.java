package test;

class B implements Iab
{
    @Override
    public int a(int p1, float p2)
    {
        hello();
    }

    @Override
    public  void b()
    {
        hi();
    }

    void c()
    {
        // Not going to extract this
    }
}
