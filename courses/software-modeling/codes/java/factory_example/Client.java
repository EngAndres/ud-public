import ShoppingStore;

public Class Client{

    public static void main(String []args){
        ShoppingStore store = new ShoppingStore(){};

        int option = 0
        menu = "1. Chair\t2. Shoes\t3. Exit"
        System.out.println(menu)
        //option = // TODO add scanner
        while(option != 3){
            if(option == 1){
                Product product = store.createProduct("chair");
                product.showDescription();
            }
            else if(option == 2){
                Product proeduct = store.createProduct("shoes");
                product.showDescription();
            }
            else if(option == 3){
                System.exit(0);
            }
            //option = // TODO add scanner
        }
    }
}