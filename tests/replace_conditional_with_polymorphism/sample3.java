public class SwitchDemo3 {
    public int myMethod(String numb) {

        int mnth = 8;
        String monthString;
        switch (mnth) {
            case 1:  monthString = "January";
                     break;
            case 2:  monthString = "February";
                     break;
            case 8:  monthString = "August";
                     break;
            case 9:  monthString = "September";
                     break;
            case 10: monthString = "October";
                     break;
            case 11: monthString = "November";
                     break;
            case 12: monthString = "December";
                     break;
            default: monthString = "Invalid month";
                     break;
        }
    }
}