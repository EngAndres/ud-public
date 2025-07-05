import java.awt.BorderLayout;
import java.util.ArrayList;
import java.util.List;

import javax.swing.DefaultComboBoxModel;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.SwingUtilities;

public class App extends JFrame {
    
    private List<Category> categories;
    private List<Exhibition> exhibitions;
    private JComboBox<Exhibition> cbxExhibitions;
    private JPanel artWorksPanel;
    private DefaultComboBoxModel<Exhibition> comboModel;

    public App(){
        this.categories = new ArrayList<>();
        this.exhibitions = new ArrayList<>();

        setTitle("Art Museum Gallery");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setSize(800, 600);
        setLayout(new BorderLayout());

        // Menu
        JPanel menu = new JPanel();
        JButton btnAddCategory = new JButton("Add Category");
        JButton btnAddExhibition = new JButton("Add Exhibition");
        JButton btnAddArtWork = new JButton("Add ArtWork");
        this.comboModel = new DefaultComboBoxModel<>();
        this.cbxExhibitions = new JComboBox<>(comboModel);

        setVisible(true);
    }

    public static void main(String[] args){
        SwingUtilities.invokeLater(App::new);
    }
}
