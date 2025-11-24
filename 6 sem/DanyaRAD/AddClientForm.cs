using System;
using Npgsql;
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
    public partial class AddClientForm : Form
    {
        NpgsqlConnection con;
        int id;
        public AddClientForm(NpgsqlConnection con, int id)
        {
            InitializeComponent();
            this.con = con;
            this.id = id;
        }

        public AddClientForm(NpgsqlConnection con, int id, string name, string address, string phone)
        {
            InitializeComponent();
            this.con = con;
            this.id = id;
            textName.Text = name;
            textAddress.Text = address;
            textPhone.Text = phone;
            buttonYes.Text = "Изменить";
            buttonYes.BackColor = Color.Yellow;
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
                    = new NpgsqlCommand("insert into Clients (name, address, phone) values (:name, :address, :phone)", con);
                    command.Parameters.AddWithValue("name", textName.Text);
                    command.Parameters.AddWithValue("address", textAddress.Text);
                    command.Parameters.AddWithValue("phone", textPhone.Text);
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
                    = new NpgsqlCommand("update Clients set name=:name, address=:address, phone=:phone where id=:id", con);
                    command.Parameters.AddWithValue("name", textName.Text);
                    command.Parameters.AddWithValue("address", textAddress.Text);
                    command.Parameters.AddWithValue("phone", textPhone.Text);
                    command.Parameters.AddWithValue("id", id);
                    command.ExecuteNonQuery();
                    Close();
                }
                catch { }
            }
        }
    }
}
