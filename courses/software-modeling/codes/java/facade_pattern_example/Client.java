public class Client {
    public static void main(String[] args) {
        ManageBankAccount manageBankAccount = new ManageBankAccount();
        manageBankAccount.login("admin", "admin");
        manageBankAccount.addCreditCard();
        manageBankAccount.addSavingAccount();
        System.out.println("Balance: " + manageBankAccount.getBalance());
    }
}