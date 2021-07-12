public class SwitchDemo4 {
    public int myMethod4(int numb) {

        int mnth = 8;
        String monthString;
        switch (mnth) {
            case 1:  monthString = "January";
                     int s = 2;
                     break;
            default: monthString = "Invalid month";
                     break;
        }
    }
}