/* Before refactoring (Original version) */
class A_New extends A
{
    public string h;

    void printH(){
        print(this.h);
    }
}
class A
{
    public int f; /* printF , printF, */
    public int g; /* printF, printG */

    // Method 1
    public void printF(int i)
    {
        this.f += i * this.f;
        if(this.f) {
            print(this.f);
        }
    }

    // Method 2
    public void printF(float i){
        this.f = (int) (i * this.f);
        this.g = (int) (i * this.g);
    }

    // Method 3
    void printG(){
        print(this.g);
    }
    static void m4() {
        f = 10;
        if(f >= 10) {
            print(f);
            f += 1;
        }
    }
}
