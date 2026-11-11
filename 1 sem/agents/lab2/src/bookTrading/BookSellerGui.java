package bookTrading;

import java.awt.BorderLayout;
import java.awt.GridLayout;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.WindowConstants;

public class BookSellerGui extends JFrame {
    private final BookSellerAgent agent;
    private final JTextField titleField = new JTextField(18);
    private final JTextField priceField = new JTextField(18);

    public BookSellerGui(BookSellerAgent agent) {
        super("Продавец: " + agent.getLocalName());
        this.agent = agent;

        setLayout(new BorderLayout(8, 8));

        JPanel form = new JPanel(new GridLayout(2, 2, 6, 6));
        form.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        form.add(new JLabel("Название книги:"));
        form.add(titleField);
        form.add(new JLabel("Цена:"));
        form.add(priceField);

        JButton addButton = new JButton("Добавить книгу");
        addButton.addActionListener(e -> addBook());

        add(form, BorderLayout.CENTER);
        add(addButton, BorderLayout.SOUTH);

        // Закрытие окна завершает агента-продавца
        setDefaultCloseOperation(WindowConstants.DO_NOTHING_ON_CLOSE);
        addWindowListener(new WindowAdapter() {
            @Override
            public void windowClosing(WindowEvent e) {
                agent.doDelete();
            }
        });

        pack();
        setLocationRelativeTo(null);
    }

    private void addBook() {
        String title = titleField.getText().trim().replaceAll("\\s+", "_");
        String priceText = priceField.getText().trim();

        if (title.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Введите название книги.");
            return;
        }

        try {
            int price = Integer.parseInt(priceText);
            if (price < 0) {
                JOptionPane.showMessageDialog(this, "Цена не может быть отрицательной.");
                return;
            }

            agent.updateCatalogue(title, price);
            titleField.setText("");
            priceField.setText("");
        } catch (NumberFormatException e) {
            JOptionPane.showMessageDialog(this, "Цена должна быть целым числом.");
        }
    }
}