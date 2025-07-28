//ComputerPart.java
class ComputerPart {
   public void DisplayingKeyboard() {
      System.out.println("Displaying Keyboard.");
   }
      public void DisplayingMonitor() {
      System.out.println("Displaying Monitor.");
   }
   public void DisplayingMouse() {
      System.out.println("Displaying Mouse.");
   }
   public void DisplayingComputer() {
      System.out.println("Displaying Computer.");
   }
}
//Keyboard.java
class Keyboard extends ComputerPart {
}
//Monitor.java
class Monitor extends ComputerPart {
}
//Mouse.java
class Mouse extends ComputerPart {
}
//Computer.java
class Computer extends ComputerPart {
}
//main
public class Main {
   public static void main(String[] args) {
     Keyboard obj1 = new Keyboard();
     Monitor obj2 = new Monitor();
     Mouse obj3 = new Mouse();
     Computer obj4 = new Computer();
     obj1.DisplayingKeyboard();
     obj2.DisplayingMonitor();
     obj3.DisplayingMouse();
     obj4.DisplayingComputer();
    }
}

