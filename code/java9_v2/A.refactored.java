/*After refactoring (Refactored version)*/
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

void m(int i)
    {
        this.setF(i * this.getF());
    }
}
