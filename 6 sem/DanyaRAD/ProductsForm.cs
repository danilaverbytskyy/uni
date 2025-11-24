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
    public partial class ProductsForm : Form
    {
        public NpgsqlConnection con;
        DataTable dt;
        DataSet ds;
        public ProductsForm(NpgsqlConnection con)
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
            SELECT id,
            title as ""Название"",
            ed as ""Ед.Изм.""
            FROM Products 
            order by id
            ";
            NpgsqlDataAdapter da = new NpgsqlDataAdapter(sql, con);
            ds.Reset();
            da.Fill(ds);
            dt = ds.Tables[0];
            dataGridView1.DataSource = dt;
            this.StartPosition = FormStartPosition.CenterScreen;
        }

        private void exitToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Close();
        }

        private void deleteToolStripMenuItem_Click(object sender, EventArgs e)
        {
            var id = (int)dataGridView1.CurrentRow.Cells["ID"].Value;
            var command
                = new NpgsqlCommand("delete from Products where id=:id", con);
            command.Parameters.AddWithValue("id", id);
            command.ExecuteNonQuery();
            UpdateData();
        }

        private void addToolStripMenuItem_Click(object sender, EventArgs e)
        {
            AddProductForm addProductForm = new AddProductForm(con, -1);
            addProductForm.ShowDialog();
            UpdateData();
        }

        private void editToolStripMenuItem_Click(object sender, EventArgs e)
        {
            int id = (int)dataGridView1.CurrentRow.Cells["ID"].Value;
            string title = (string)dataGridView1.CurrentRow.Cells["Название"].Value;
            string ed = (string)dataGridView1.CurrentRow.Cells["Ед.Изм."].Value;
            AddProductForm addProductForm = new AddProductForm(con, id, title, ed);
            addProductForm.ShowDialog();
            UpdateData();
        }

        private void buttonFormReport_Click(object sender, EventArgs e)
        {
            var dateForProductsReportForm = new ChooseDateForProductsReportForm(con);
            dateForProductsReportForm.ShowDialog();

            if (dateForProductsReportForm.IsReportCreated)
            {
                DateTime leftBorderDate = dateForProductsReportForm.leftBorderDate;
                DateTime rightBorderDate = dateForProductsReportForm.rightBorderDate;

                string sql = @"
SELECT 
    p.title AS ""Название товара"",
    p.ed AS ""Единица измерения"",
    SUM(op.price * op.quantity) AS ""Общая сумма"",
    COUNT(op.order_id) AS ""Количество заказов"",
    SUM(CASE WHEN op.isDelivered THEN 1 ELSE 0 END) AS ""Доставлено"",
    SUM(CASE WHEN NOT op.isDelivered THEN 1 ELSE 0 END) AS ""Не доставлено""
FROM 
    Products p
LEFT JOIN 
    Orders_Products op ON p.id = op.product_id
LEFT JOIN 
    Orders o ON op.order_id = o.id
WHERE 
    o.date >= @leftBorderDate AND o.date <= @rightBorderDate
GROUP BY 
    p.title, p.ed
ORDER BY 
    ""Общая сумма"" DESC;";

                NpgsqlDataAdapter da = new NpgsqlDataAdapter(sql, con);
                da.SelectCommand.Parameters.AddWithValue("@leftBorderDate", NpgsqlTypes.NpgsqlDbType.Date, leftBorderDate);
                da.SelectCommand.Parameters.AddWithValue("@rightBorderDate", NpgsqlTypes.NpgsqlDbType.Date, rightBorderDate);

                ds.Reset();
                da.Fill(ds);
                dt = ds.Tables[0];
                dataGridView1.DataSource = dt;
                this.StartPosition = FormStartPosition.CenterScreen;
            }
        }
    }
}
