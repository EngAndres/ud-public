import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.ArrayList;

public class App {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame frame = new JFrame("Food Store");
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.setSize(600, 400);

            // Shopping cart logic
            ShoopingCart cart = new ShoopingCart();
            DefaultListModel<String> cartModel = new DefaultListModel<>();
            JList<String> cartList = new JList<>(cartModel);

            // Left panel: Product menu
            JPanel menuPanel = new JPanel();
            menuPanel.setLayout(new BoxLayout(menuPanel, BoxLayout.Y_AXIS));

            JButton pizzaBtn = new JButton("Add Pizza");
            pizzaBtn.addActionListener(e -> {
                String flavor = JOptionPane.showInputDialog(frame, "Pizza flavor:");
                String sizeStr = JOptionPane.showInputDialog(frame, "Pizza size:");
                String daysStr = JOptionPane.showInputDialog(frame, "Days since preparation:");
                if (flavor != null && sizeStr != null && daysStr != null) {
                    try {
                        int size = Integer.parseInt(sizeStr);
                        int days = Integer.parseInt(daysStr);
                        Pizza pizza = new Pizza(flavor, size, days);
                        cart.addProduct(pizza);
                        cartModel.addElement(pizza.toString());
                    } catch (Exception ex) {
                        JOptionPane.showMessageDialog(frame, "Invalid input.");
                    }
                }
            });

            JButton burgerBtn = new JButton("Add Burger");
            burgerBtn.addActionListener(e -> {
                String weightStr = JOptionPane.showInputDialog(frame, "Burger weight:");
                if (weightStr != null) {
                    try {
                        int weight = Integer.parseInt(weightStr);
                        Burguer burger = new Burguer(weight);
                        cart.addProduct(burger);
                        cartModel.addElement(burger.toString());
                    } catch (Exception ex) {
                        JOptionPane.showMessageDialog(frame, "Invalid input.");
                    }
                }
            });

            JButton hotdogBtn = new JButton("Add Hotdog");
            hotdogBtn.addActionListener(e -> {
                String sausage = JOptionPane.showInputDialog(frame, "Sausage type:");
                String daysStr = JOptionPane.showInputDialog(frame, "Days since preparation:");
                if (sausage != null && daysStr != null) {
                    try {
                        int days = Integer.parseInt(daysStr);
                        Hotdog hotdog = new Hotdog(sausage, days);
                        cart.addProduct(hotdog);
                        cartModel.addElement(hotdog.toString());
                    } catch (Exception ex) {
                        JOptionPane.showMessageDialog(frame, "Invalid input.");
                    }
                }
            });

            menuPanel.add(pizzaBtn);
            menuPanel.add(burgerBtn);
            menuPanel.add(hotdogBtn);

            // Right panel: Shopping cart
            JPanel cartPanel = new JPanel(new BorderLayout());
            cartPanel.add(new JLabel("Shopping Cart:"), BorderLayout.NORTH);
            cartPanel.add(new JScrollPane(cartList), BorderLayout.CENTER);

            // Layout
            frame.setLayout(new GridLayout(1, 2));
            frame.add(menuPanel);
            frame.add(cartPanel);

            frame.setVisible(true);
        });
    }
}