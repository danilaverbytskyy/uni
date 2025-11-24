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
    public partial class AddProductForm : Form
    {
        NpgsqlConnection con;
        int id;
        public AddProductForm(NpgsqlConnection con, int id)
        {
            InitializeComponent();
            this.con = con;
            this.id = id;
        }

        private void AddProductForm_Load(object sender, EventArgs e)
        {

        }

        public AddProductForm(NpgsqlConnection con, int id, string title, string ed)
        {
            InitializeComponent();
            this.con = con;
            this.id = id;
            textName.Text = title;
            textAddress.Text = ed;
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
                    = new NpgsqlCommand("insert into Products (title, ed) values (:title, :ed)", con);
                    command.Parameters.AddWithValue("title", textName.Text);
                    command.Parameters.AddWithValue("ed", textAddress.Text);
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
                    = new NpgsqlCommand("update Products set title=:title, ed=:ed where id=:id", con);
                    command.Parameters.AddWithValue("title", textName.Text);
                    command.Parameters.AddWithValue("ed", textAddress.Text);
                    command.Parameters.AddWithValue("id", id);
                    command.ExecuteNonQuery();
                    Close();
                }
                catch { }
            }
        }
    }
}
