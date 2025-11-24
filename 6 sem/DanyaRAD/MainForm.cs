using Npgsql;

namespace DanyaRAD2
{
    public partial class MainForm : Form
    {
        public NpgsqlConnection con;

        public MainForm()
        {
            MyLoad();
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        public void MyLoad()
        {
            this.StartPosition = FormStartPosition.CenterScreen;
            con = new NpgsqlConnection("Server=localhost;Port=5432;UserID=postgres;Password=password;Database=DanyaRAD");
            con.Open();
        }

        public void ButtonClients_Click(object sender, EventArgs e)
        {
            try
            {
                ClientsForm clientsForm = new ClientsForm(con);
                clientsForm.ShowDialog();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка: {ex.Message}", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void buttonProducts_Click(object sender, EventArgs e)
        {
            ProductsForm productsForm = new ProductsForm(con);
            productsForm.ShowDialog();
        }

        private void buttonOrders_Click(object sender, EventArgs e)
        {
            OrdersForm ordersForm = new OrdersForm(con);
            ordersForm.ShowDialog();
        }
    }
}
