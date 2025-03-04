using Microsoft.VisualBasic.ApplicationServices;
using System.Windows.Forms;

namespace DanyaRAD
{
    public partial class Form1 : Form
    {
        private String text;
        private List<User> users;
        public Form1()
        {
            users = new List<User>();
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            text = "";
            richTextBox1.Text = "";

            String fio = textBoxFIO.Text;
            if (fio.Length == 0)
            {
                fio = "имя не указано";
            }
            text += "ФИО: " + fio + "\n";
            String address = comboBoxCity.Text;
            if (address.Length > 0)
            {
                text += "Адрес: " + address + "\n";
            }
            if (radioButtonMale.Checked)
            {
                text += "Пол мужской\n";
            }
            if (radioButtonFemale.Checked)
            {
                text += "Пол женский\n";
            }
            text += "Секции: ";
            for (int i = 0; i < checkedListBoxSections.CheckedItems.Count; i++)
            {
                text += checkedListBoxSections.CheckedItems[i].ToString() + " ";
            }
            text += "\n";
            richTextBox1.AppendText(text);
            MessageBox.Show("Данные сохранены");
        }

        private void textBoxFIO_TextChanged(object sender, EventArgs e)
        {

        }

        private void radioButtonMale_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void radioButtonFemale_CheckedChanged(object sender, EventArgs e)
        {

        }
    }
}
