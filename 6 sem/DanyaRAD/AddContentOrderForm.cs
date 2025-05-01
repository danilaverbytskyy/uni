using Npgsql;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace DanyaRAD2
{
    public partial class AddContentOrderForm : Form
    {
        NpgsqlConnection con;
        int id;
        DataTable dt;
        DataSet ds;
        public AddContentOrderForm(NpgsqlConnection con, int id)
        {
            InitializeComponent();
            this.con = con;
            this.id = id;
            OrderIdLabel.Text = "" + id;
            dt = new DataTable();
            ds = new DataSet();
            Update();
        }

        private void Update()
        {
            string sql = "select * from Products"; // Товары для формы
            NpgsqlDataAdapter da = new NpgsqlDataAdapter(sql, con);
            ds.Reset();
            da.Fill(ds);
            dt = ds.Tables[0];
            comboBoxProducts.DataSource = dt;
            comboBoxProducts.DisplayMember = "title";
            comboBoxProducts.ValueMember = "id";
        }

        private void buttonYes_Click(object sender, EventArgs e)
        {
            try
            {
                var command
                = new NpgsqlCommand("insert into Orders_Products(order_id, product_id, price, quantity, isdelivered) values (:order_id, :product_id, :price, :quantity, :isdelivered)", con);
                command.Parameters.AddWithValue("order_id", id);
                command.Parameters.AddWithValue("product_id", comboBoxProducts.SelectedValue);
                command.Parameters.AddWithValue("price", Convert.ToInt32(textBoxPrice.Text));
                command.Parameters.AddWithValue("quantity", Convert.ToInt32(textBoxQuantity.Text));
                command.Parameters.AddWithValue("isdelivered", checkBoxDelivered.Checked);
                command.ExecuteNonQuery();
                Close();
            }
            catch { }
        }
        

        private void buttonNo_Click(object sender, EventArgs e)
        {
            Close();
        }
    }
}
