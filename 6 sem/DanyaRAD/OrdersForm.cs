using Npgsql;
using Microsoft.Office.Interop.Excel;
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
    public partial class OrdersForm : Form
    {
        public NpgsqlConnection con;
        System.Data.DataTable dt;
        DataSet ds;
        System.Data.DataTable dt2;
        DataSet ds2;
        public OrdersForm(NpgsqlConnection con)
        {
            this.con = con;
            dt = new System.Data.DataTable();
            ds = new DataSet();
            dt2 = new System.Data.DataTable();
            ds2 = new DataSet();
            InitializeComponent();
            UpdateData();
        }

        private void OrdersForm_Load(object sender, EventArgs e)
        {

        }

        public void UpdateData()
        {
            String sql = @"
            SELECT id, 
            (select name from Clients where id=client_id) as ""Имя"", 
            total_price ""Полная сумма"", 
            date ""Дата""
            FROM Orders 
            order by id";
            NpgsqlDataAdapter da = new NpgsqlDataAdapter(sql, con);
            ds.Reset();
            da.Fill(ds);
            dt = ds.Tables[0];
            dataGridView1.DataSource = dt;
            this.StartPosition = FormStartPosition.CenterScreen;
        }

        public void UpdateData2(int id)
        {
            String sql = @"SELECT 
            id, 
            (select title from Products where id=product_id) as ""Название"", 
            price as ""Цена"", 
            quantity as ""Количество"", 
            isdelivered as ""Доставлено""
            FROM Orders_Products 
            where order_id=" + id + " " +
            "order by id";
            NpgsqlDataAdapter da = new NpgsqlDataAdapter(sql, con);
            ds2.Reset();
            da.Fill(ds2);
            dt2 = ds2.Tables[0];
            dataGridView2.DataSource = dt2;
            this.StartPosition = FormStartPosition.CenterScreen;
        }

        private void deleteToolStripMenuItem_Click(object sender, EventArgs e)
        {
            var id = (int)dataGridView1.CurrentRow.Cells["ID"].Value;
            var command
                = new NpgsqlCommand("delete from Orders_Products where order_id=:id", con);
            command.Parameters.AddWithValue("id", id);
            command.ExecuteNonQuery();
            var command2
                = new NpgsqlCommand("delete from Orders where id=:id", con);
            command2.Parameters.AddWithValue("id", id);
            command2.ExecuteNonQuery();
            UpdateData();
            UpdateData2(id);
        }

        private void exitToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Close();
        }

        private void addToolStripMenuItem_Click(object sender, EventArgs e)
        {
            AddOrderForm addOrderForm = new AddOrderForm(con, -1);
            addOrderForm.ShowDialog();
            UpdateData();
        }

        private void editToolStripMenuItem_Click(object sender, EventArgs e)
        {
            int id = (int)dataGridView1.CurrentRow.Cells["ID"].Value;
            int total_price = (int)dataGridView1.CurrentRow.Cells["Полная сумма"].Value;
            DateTime date = (DateTime)dataGridView1.CurrentRow.Cells["Дата"].Value;

            // Разбираемся с id клиента по его имени
            String sql = "SELECT id from Clients where name='" + (string)dataGridView1.CurrentRow.Cells["name"].Value + "'";
            NpgsqlDataAdapter da = new NpgsqlDataAdapter(sql, con);
            ds.Reset();
            da.Fill(ds);
            int client_id = Convert.ToInt32(ds.Tables[0].Rows[0]["id"]);

            AddOrderForm addOrderForm = new AddOrderForm(con, id, client_id, total_price, date);
            addOrderForm.ShowDialog();
            UpdateData();
        }

        private void dataGridView1_CellClick(object sender, DataGridViewCellEventArgs e)
        {
            int id = (int)dataGridView1.CurrentRow.Cells["ID"].Value;
            UpdateData2(id);
        }

        private void contentToolStripMenuItem_Click_Add(object sender, EventArgs e)
        {
            int id = (int)dataGridView1.CurrentRow.Cells["ID"].Value;
            AddContentOrderForm addContentOrderForm = new AddContentOrderForm(con, id);
            addContentOrderForm.ShowDialog();
            UpdateData();
        }

        private void contentToolStripMenuItem1_Click_Delete(object sender, EventArgs e)
        {
            if (dataGridView2.CurrentRow == null)
            {
                return;
            }
            var id = (int)dataGridView2.CurrentRow.Cells["ID"].Value;
            var command
                = new NpgsqlCommand("delete from Orders_Products where id=:id", con);
            command.Parameters.AddWithValue("id", id);
            command.ExecuteNonQuery();
            UpdateData2(id);
            UpdateData();
        }

        private void buttonExportExcel_Click(object sender, EventArgs e)
        {
            try
            {
                OpenFileDialog ofd = new OpenFileDialog();
                ofd.ShowDialog();
                String fileName = ofd.FileName;

                Microsoft.Office.Interop.Excel.Application excelObj = new Microsoft.Office.Interop.Excel.Application();
                excelObj.Visible = true;

                Workbook wb = excelObj.Workbooks.Open(fileName, 0, false, 5, "", "", false,
                    XlPlatform.xlWindows, "", true, false, 0, true, false, false);

                Worksheet worksheet = (Worksheet)wb.Sheets[1];

                worksheet.Cells[1, 1].Value = "Дата";
                worksheet.Cells[1, 2].Value = dataGridView1.CurrentRow.Cells["дата"].Value;
                worksheet.Cells[2, 1].Value = "Клиент";
                worksheet.Cells[2, 2].Value = dataGridView1.CurrentRow.Cells["имя"].Value;
                worksheet.Cells[3, 1].Value = "Полная сумма";
                worksheet.Cells[3, 2].Value = dataGridView1.CurrentRow.Cells["полная сумма"].Value;

                int rowIndex = 3;
                for (int i = 0; i < dataGridView2.Columns.Count; i++)
                {
                    worksheet.Cells[1+ rowIndex, i + 1].Value = dataGridView2.Columns[i].HeaderText;
                    if (i + 1 == dataGridView2.Columns.Count)
                    {
                        worksheet.Cells[1 + rowIndex, i + 2].Value = ""; // костыль чтоб не двоился один из заголовков
                    }
                }

                for (int i = 0; i < dataGridView2.Rows.Count; i++)
                {
                    if (dataGridView2.Rows[i].IsNewRow)
                    {
                        continue;
                    }

                    for (int j = 0; j < dataGridView2.Columns.Count; j++)
                    {
                        worksheet.Cells[i + 2 + rowIndex, j + 1].Value = dataGridView2.Rows[i].Cells[j].Value?.ToString();
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка: {ex.Message}");
            }
        }

        private void изменитьДоставленностьToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if (dataGridView2.CurrentRow == null)
            {
                return;
            }
            var id = (int)dataGridView2.CurrentRow.Cells["ID"].Value;
            var command
                = new NpgsqlCommand("update orders_products set isdelivered=not(isdelivered) where id=:id", con);
            command.Parameters.AddWithValue("id", id);
            command.ExecuteNonQuery();
            UpdateData2(id);
            UpdateData();
        }
    }
}
