/* Before refactoring (Original version) */
class A
{
    public int f; /* public field */
    void m(int i)
    {
        this.f = i * this.f;
    }
}
