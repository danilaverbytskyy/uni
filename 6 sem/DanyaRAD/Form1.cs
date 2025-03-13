using DanyaRAD.models;
using Microsoft.VisualBasic.ApplicationServices;
using System.Windows.Forms;

namespace DanyaRAD
{
    public partial class Form1 : Form
    {
        private String text;
        private List<MyUser> users;
        public Form1()
        {
            users = new List<MyUser>();
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            text = "";
            richTextBox1.Text = "";

            MyUser user = new MyUser();

            String fio = textBoxFIO.Text;
            if (fio.Length == 0)
            {
                fio = "имя не указано";
            }
            user.setFio(fio);
            String address = comboBoxCity.Text;
            user.setaddress(address);
            if (radioButtonMale.Checked)
            {
                user.setsex(1);
            }
            if (radioButtonFemale.Checked)
            {
                user.setsex(2);
            }

            user.setHobbies(new List<string>());
            for (int i = 0; i < checkedListBoxSections.CheckedItems.Count; i++)
            {
                String item = checkedListBoxSections.CheckedItems[i].ToString();
                
                if (item == null)
                    continue;
                user.addHobby(item);
            }
            users.Add(user);
            for (int i = 0; i < users.Count; i++)
            {
                richTextBox1.AppendText("User #"+ i + "\n" + users[i].getInfo());
            }
            MessageBox.Show("Данные добавлены");
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
