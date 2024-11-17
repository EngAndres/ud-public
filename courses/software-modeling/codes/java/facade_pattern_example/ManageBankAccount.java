import java.util.ArrayList;
import CreditCards;
import SavingAccount;
import Authentication;

public class ManageBankAccount{

    private boolean status;
    private ArrayList<CreditCards> creditCards;
    private ArrayList<SavingAccount> savingAccount;

    public ManageBankAccount(){
        this.status = false;
        this.creditCards = new ArrayList<CreditCards>();
        this.savingAccount = new ArrayList<SavingAccount>();
    }

    public void login(String username, String password){
        this.status = Authentication.auth(username, password);
    }

    public void addCreditCard(){
        int cardNumber = 123456;
        int maximumLimit = 1000;

        CreditCards creditCard = new CreditCards(cardNumber, maximumLimit);
        this.creditCards.add(creditCard);
    }

    public void addSavingAccount(){
        SavingAccount savingAccount = new SavingAccount();
        this.savingAccount.add(savingAccount);
    }

    public int getBalance(){
        int debt = 0;
        for(CreditCards creditCard : this.creditCards){
            debt += creditCard.getMoney();
        }
        int money = 0;
        for(SavingAccount sa = this.savingAccount){
            money += sa.getMoney();
        }
        return money - debt;
    }
}