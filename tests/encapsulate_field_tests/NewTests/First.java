package learnjava;

public class First{
    private int score;
	// new getter method
	public int getScore() { 
		return this.score;
	}

	// new setter method
	public void setScore(int score) { 
		this.score = score;
	}

    public void msg() {
        System.out.println("Hello");
    }
}