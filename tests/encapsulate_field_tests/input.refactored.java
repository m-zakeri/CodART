/*After refactoring (Refactored version)*/
class A_New extends A
{
    public string h;

    void printH(){
        print(this.h);
    }
}
class A
{
    private int f;
	public int getF() { 
		 return this.f;
	}
	public void setF(int f) { 
		this.f = f;
	}
	/*End of accessor and mutator methods!*/

public int g; /* printF, printG */

    // Method 1
    public void printF(int i)
    {
        this.setF(i * this.getF());
    }

    // Method 2
    public void printF(float i){
        this.setF((int) (i * this.getF()));
        this.g = (int) (i * this.g);
    }

    // Method 3
    void printG(){
        print(this.g);
    }
}
