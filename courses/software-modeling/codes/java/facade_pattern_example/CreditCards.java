public class CreditCards {
    
    private int cardNumber;
    private int maximumLimit;
    private int money;

    public CreditCards(int cardNumber, int maximumLimit) {
        this.cardNumber = cardNumber;
        this.maximumLimit = maximumLimit;
        this.money = 0;
    }

    public void withdrawMoney(int amount) {
        if (amount + this.money <= maximumLimit) {
            money += amount;
            System.out.println("Money withdrawn: " + amount);
        } else {
            System.out.println("You have reached your maximum limit.");
        }
    }

    public int getAvailableMoney() {
        return this.maximumLimit - this.money;
    }

    public int getMoney() {
        return this.money;
    }
}