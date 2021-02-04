/* Before refactoring (Original version) */
class A
{
    public int f; /* printF , printF, */
    public int g; /* printF, printG */
    public string h; /* printH */

    // Method 1
    void printF(int i)
    {
        this.f = i * this.f;
    }

    // Method 2
    void printF(float i){
        this.f = (int) (i * this.f);
        this.g = (int) (i * this.g);
    }

    // Method 3
    void printG(){
        print(this.g);
    }

    // Method 4
    void printH(){
        print(this.h);
    }
}


class B{

    public string instance;

    public B(){
        A a = new A(); // should change
        this.instance = a.h;
        this.c();
        a.printH();
    }

    void c(){
        A a = new A(); // should not change
        int j = a.f;
        // not refactoring is better than error
        // a.printH();
    }
}