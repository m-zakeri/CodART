class a{
    int main(){
        try {
            int[] myNumbers = {1, 2, 3};
            System.out.println(myNumbers[10]);
        }
        catch (Exception e) {
            if (a>1){
                System.out.println("Something went wrong.");
            }
            else{
                a++;
            }
         }
        catch(ArrayIndexOutOfBoundsException | ArithmeticException exp) {
            if (a>1){
                System.out.println("Something went wrong.");
            }
            else{
                a++;
            }
          }

   }

}