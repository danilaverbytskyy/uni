using Npgsql;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Windows.Forms.DataVisualization.Charting;
using System.Windows.Forms;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace DanyaRAD2
{
    public partial class ClientsForm : Form
    {
        public NpgsqlConnection con;
        DataTable dt;
        DataSet ds;
        public ClientsForm(NpgsqlConnection con)
        {
            this.con = con;
            dt = new DataTable();
            ds = new DataSet();
            InitializeComponent();
            UpdateData();
        }

        public void UpdateData()
        {
            String sql = @"
                SELECT 
                id,
                name as ""Имя"",
                address as ""Адрес"",
                phone as ""Телефон""
                FROM Clients 
                order by id
                ";
            NpgsqlDataAdapter da = new NpgsqlDataAdapter(sql, con);
            ds.Reset();
            da.Fill(ds);
            dt = ds.Tables[0];
            dataGridView1.DataSource = dt;
            this.StartPosition = FormStartPosition.CenterScreen;
        }

        private void Form2_Load(object sender, EventArgs e)
        {

        }

        private void deleteToolStripMenuItem_Click(object sender, EventArgs e)
        {
            var id = (int)dataGridView1.CurrentRow.Cells["ID"].Value;
            var command
                = new NpgsqlCommand("delete from Clients where id=:id", con);
            command.Parameters.AddWithValue("id", id);
            command.ExecuteNonQuery();
            UpdateData();
        }

        private void exitToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Close();
        }

        private void addToolStripMenuItem_Click(object sender, EventArgs e)
        {
            AddClientForm addClientForm = new AddClientForm(con, -1);
            addClientForm.ShowDialog();
            UpdateData();
        }

        private void editToolStripMenuItem_Click(object sender, EventArgs e)
        {
            int id = (int)dataGridView1.CurrentRow.Cells["ID"].Value;
            string name = (string)dataGridView1.CurrentRow.Cells["имя"].Value;
            string address = (string)dataGridView1.CurrentRow.Cells["адрес"].Value;
            string phone = (string)dataGridView1.CurrentRow.Cells["телефон"].Value;
            AddClientForm addClientForm = new AddClientForm(con, id, name, address, phone);
            addClientForm.ShowDialog();
            UpdateData();
        }

        private void buttonCreateDiagram_Click(object sender, EventArgs e)
        {
            ChooseClientsAndDateForDiagramForm preDiagramForm = new ChooseClientsAndDateForDiagramForm(con);
            preDiagramForm.ShowDialog();
        }
    }
}
