/* Before refactoring (Original version) */
class A
{
    public int f; /* public field */
    public int g;
    public float k;
    public float t;

    void m(int i)
    {
        // works on f,k
        this.f = i * this.f;
        this.k = 67 + this.f;
    }

    int m2(float j)
    {
        // works on t,g
        this.g = j*2 ;
        this.t = this.g * 3;
    }
}

class B
{
    public B()
    {
        A instance = new A();
        instance.m2(2.3);
    }

    void j()
    {
        new A().m2(3.5);
    }
}
