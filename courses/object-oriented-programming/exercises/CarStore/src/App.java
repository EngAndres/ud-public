import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class App {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame frame = new JFrame("Car Store Catalog");
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.setSize(600, 400);

             
            Catalog catalog = new Catalog(); 
            
            JList<String> carList = new JList<>(catalog.cars.stream()
                    .map(Car::toString) // Adjust toString method in Car class as needed
                    .toArray(String[]::new));
            
            JTextArea carDetails = new JTextArea();
            carDetails.setEditable(false);

            carList.addListSelectionListener(e -> {
                int idx = carList.getSelectedIndex();
                if (idx >= 0) {
                    Car selectedCar = catalog.cars.get(idx);
                    carDetails.setText(selectedCar.toString()); // Adjust as needed
                }
            });

            frame.setLayout(new BorderLayout());
            frame.add(new JScrollPane(carList), BorderLayout.WEST);
            frame.add(new JScrollPane(carDetails), BorderLayout.CENTER);

            frame.setVisible(true);

            JButton addButton = new JButton("Add Car");
            addButton.addActionListener(e -> {
                JTextField ccField = new JTextField();
                JTextField chassisField = new JTextField();
                JTextField colorField = new JTextField();
                JPanel panel = new JPanel(new GridLayout(0, 1));
                panel.add(new JLabel("CC:"));
                panel.add(ccField);
                panel.add(new JLabel("Chassis Type:"));
                panel.add(chassisField);
                panel.add(new JLabel("Color:"));
                panel.add(colorField);

                int result = JOptionPane.showConfirmDialog(frame, panel, "Add New Car",
                        JOptionPane.OK_CANCEL_OPTION, JOptionPane.PLAIN_MESSAGE);
                if (result == JOptionPane.OK_OPTION) {
                    Integer cc = Integer.parseInt(ccField.getText());
                    String chassis = chassisField.getText();
                    String color = colorField.getText();
                    try {
                        Car newCar = new Car(cc, chassis, color);
                        catalog.cars.add(newCar);
                        carList.setListData(catalog.cars.stream()
                                .map(Car::toString)
                                .toArray(String[]::new));
                    } catch (NumberFormatException ex) {
                        JOptionPane.showMessageDialog(frame, "Car  cannot be created.");
                    }
                }
            });

            JPanel topPanel = new JPanel();
            topPanel.add(addButton);

            frame.add(topPanel, BorderLayout.NORTH);
            
        });
    }
}