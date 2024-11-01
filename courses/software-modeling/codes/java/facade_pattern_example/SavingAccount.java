public class SavingAccount {

    private int money;

    public SavingAccount() {
        this.money = 0;
    }

    public void depositMoney(int amount) {
        if(amount < 0) {
            System.out.println("Invalid amount.");
        }
        else {
            self.money += amount;
            System.out.println("Money deposited: " + amount);
        }
    }

    public void withdrawMoney(int amount) {
        if (amount <= this.money) {
            this.money -= amount;
            System.out.println("Money withdrawn: " + amount);
        } else {
            System.out.println("You don't have enough money.");
        }
    }
}