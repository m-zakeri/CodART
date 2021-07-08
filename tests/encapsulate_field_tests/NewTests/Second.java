package testjava;

import learnjava.*;

class Second {  
    public static void main(String[] args) {  
        First obj = new First();
	    obj.msg();
	    obj.setScore(12);
    	System.out.println(obj.getScore());
    }  
}