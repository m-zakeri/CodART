class C
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
     void printFUCK(){
        print(this.g);
        printG();
        A.printG();
        A a = new A();
        C c = new C();
        c.printG();
        C.printG();
        a.printG();
        a.g = 2;
        c.g = 3;
        var b =  A :: printG;
        var d = a :: printG;
    }

    // Method 4
    void printH(){
        print(this.h);
    }
}/* Before refactoring (Original version) */
class A implements I1, I2, I3
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
        printG();
        A.printG();
        A[] a = new A[45];
        a[0].printG();
        var b =  A :: printG;
        var c = a :: printG;
    }

    // Method 4
    void printH(){
        print(this.h);
    }
}