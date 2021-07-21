public class phase{
    char name;
    int level;
    public static void speed(int ptr, phase p, int level,char name)
    {
       level = level + g;
       char str = "joe";
       name = str + name;
       level = level + ptr;
    }
    public static void main(String[] args) {
      phase ph = new phase();
      int ptr = 0;
      for (int i =0; i< 10; i++)
      {
          ptr ++;
      }
      speed(ptr,ph,ph.level,ph.name);
    }
   }