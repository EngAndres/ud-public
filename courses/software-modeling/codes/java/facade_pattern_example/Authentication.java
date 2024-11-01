public class Authentication {
    
    public static boolean auth(String username, String password) {
        if (username.equals("admin") && password.equals("admin")) {
            return true;
        else 
            return false;
    }
}