class phase{
    int[] array;
    void bubbleSort(Test t,int pl)
    {
		for (int i = 0; i < pl-1; i++)
            for (int j = 0; j < pl-i-1; j++)
                if (t.array[j] > t.arry[j+1])
                {
                    // swap arr[j+1] and arr[j]
                    int temp = t.array[j];
                    t.array[j] =t.array[j+1];
                    t.array[j+1] = temp;
                }
}
 class Test{
 void f1(){
         Test t = new Test();
      bubbleSort(t,t.plus);}
    int plus;
}
public static void main(String[] args) {
      phase_3 p = new phase_3();
      Test t = new Test();
      bubbleSort(t,t.plus);
    }
}