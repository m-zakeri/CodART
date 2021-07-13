public class phase{
    int name;
    int level;

    public static int speed(phase t,int level1, int name)
    {
        int i = 0;
         i = i*2;
         return i;
    }


    public static void main(String[] args) {
      phase qu = new phase();
      speed(qu,qu.level,qu.name);

    }}
