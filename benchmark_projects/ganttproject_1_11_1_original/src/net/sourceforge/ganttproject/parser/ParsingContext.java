package net.sourceforge.ganttproject.parser;

public class ParsingContext {
    public int getTaskID() {
        return myTaskID;
    }
    public void setTaskID(int id) {
        myTaskID = id;
    }
    
    private int myTaskID;
}
