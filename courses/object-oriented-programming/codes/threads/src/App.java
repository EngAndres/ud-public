public class App {
    public static void main(String[] args) throws Exception {
        Thread worker = new Thread(() -> {
            long start = System.currentTimeMillis();

            try{
                Thread.sleep(1000);
            } catch(Exception e) {}

            long end = System.currentTimeMillis();
            System.out.println("Thread time :" + (end - start)*1000);
        });

        Thread worker2 = new Thread(() -> {
            long start = System.currentTimeMillis();

            try{
                Thread.sleep(1000);
            } catch(Exception e) {}

            long end = System.currentTimeMillis();
            System.out.println("Thread time :" + (end - start)*1000);
        });

        Thread worker3 = new Thread(() -> {
            long start = System.currentTimeMillis();

            try{
                Thread.sleep(1000);
            } catch(Exception e) {}

            long end = System.currentTimeMillis();
            System.out.println("Thread time :" + (end - start)*1000);
        });

        Thread worker4 = new Thread(() -> {
            long start = System.currentTimeMillis();

            try{
                Thread.sleep(1000);
            } catch(Exception e) {}

            long end = System.currentTimeMillis();
            System.out.println("Thread time :" + (end - start)*1000);
        });

        Thread worker5 = new Thread(() -> {
            long start = System.currentTimeMillis();

            try{
                Thread.sleep(1000);
            } catch(Exception e) {}

            long end = System.currentTimeMillis();
            System.out.println("Thread time :" + (end - start)*1000);
        });

        System.out.println("Start: " + System.currentTimeMillis());
        worker.start();
        worker2.start();
        worker3.start();
        worker4.start();
        worker5.start();
        worker.join();
        System.out.println("Start: " + System.currentTimeMillis());
        
    }
    
}
