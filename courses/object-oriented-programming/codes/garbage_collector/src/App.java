public class App {
    
    public static void main(String[] args) throws Exception {
        Runtime rt = Runtime.getRuntime();
        System.out.println("Memory at the start: " + rt.freeMemory);

        for(int i = 0; i < 100000000; i++){
            String s = new String("UD 2025 OOP!");
        }

        System.out.println("Memory after the loop: " + rt.freeMemory()); 
        System.gc(); // Garbage Collector

        try{  Thread.sleep(300000);  }
        catch(Exception e){}

        System.out.println("Memory after GC: " + rt.freeMemory()); 
    }
}
