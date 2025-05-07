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
    public partial class AddOrderForm : Form
    {
        NpgsqlConnection con;
        int id;
        DataTable dt;
        DataSet ds;
        public AddOrderForm(NpgsqlConnection con, int id)
        {
            InitializeComponent();
            this.con = con;
            this.id = id;
            totalPriceLabel.Text = "0";
            dt = new DataTable();
            ds = new DataSet();
            Update();
        }

        public AddOrderForm(NpgsqlConnection con, int id, int client_id, int total_price, DateTime date)
        {
            InitializeComponent();
            this.con = con;
            this.id = id;
            dt = new DataTable();
            ds = new DataSet();
            Update();
            comboBoxClient.SelectedValue = client_id; // Обязательно после апдейта
            totalPriceLabel.Text = "" + total_price;
            dateTimePicker.Value = date;
            buttonYes.Text = "Изменить";
            buttonYes.BackColor = Color.Yellow;
        }

        private void AddOrderForm_Load(object sender, EventArgs e)
        {

        }

        private void Update()
        {
            string sql = "select * from Clients"; // Клиенты для формы
            NpgsqlDataAdapter da = new NpgsqlDataAdapter(sql, con);
            ds.Reset();
            da.Fill(ds);
            dt = ds.Tables[0];
            comboBoxClient.DataSource = dt;
            comboBoxClient.DisplayMember = "name";
            comboBoxClient.ValueMember = "id";
        }

        private void No_Click(object sender, EventArgs e)
        {
            Close();
        }

        private void Yes_Click(object sender, EventArgs e)
        {
            if (id == -1)
            {
                try
                {
                    var command
                    = new NpgsqlCommand("insert into Orders (client_id, total_price, date) values (:client_id, 0, :date)", con);
                    command.Parameters.AddWithValue("client_id", comboBoxClient.SelectedValue);
                    command.Parameters.AddWithValue("date", dateTimePicker.Value.Date);
                    command.ExecuteNonQuery();
                    Close();
                }
                catch { }
            }
            else
            {
                try
                {
                    var command
                    = new NpgsqlCommand("update Orders set client_id=:client_id, date=:date where id=:id", con);
                    command.Parameters.AddWithValue("client_id", comboBoxClient.SelectedValue);
                    command.Parameters.AddWithValue("date", dateTimePicker.Value.Date);
                    command.Parameters.AddWithValue("id", id);
                    command.ExecuteNonQuery();
                    Close();
                }
                catch { }
            }
        }
    }
}
