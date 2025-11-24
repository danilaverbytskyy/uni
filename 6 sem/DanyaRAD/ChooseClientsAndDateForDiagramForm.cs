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
using System.Windows.Forms.DataVisualization.Charting;

namespace DanyaRAD2
{
    public partial class ChooseClientsAndDateForDiagramForm : Form
    {
        public NpgsqlConnection con;
        DataTable dt;
        DataSet ds;
        private DateTime leftDateBorder;
        private DateTime rightDateBorder;

        public ChooseClientsAndDateForDiagramForm(NpgsqlConnection con)
        {
            InitializeComponent();
            this.con = con;
            dt = new DataTable();
            ds = new DataSet();
            LoadClients();
        }

        private void buttonYes_Click(object sender, EventArgs e)
        {
            // Получаем выбранные даты
            DateTime startDate = dateTimePickerLeftBorder.Value;
            DateTime endDate = dateTimePickerRightBorder.Value;

            // Получаем список выбранных клиентов
            var selectedClients = new List<string>();
            foreach (var item in checkedListBox1.CheckedItems)
            {
                selectedClients.Add(item.ToString());
            }

            if (selectedClients.Count == 0)
            {
                MessageBox.Show("Выберите хотя бы одного клиента!", "Ошибка",
                               MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            // Получаем данные из БД
            DataTable data = GetOrderDeliveryData(selectedClients, startDate, endDate);

            // Создаем форму для диаграммы
            Form chartForm = new Form();
            chartForm.Text = "Соотношение сумм заказов и доставок";
            chartForm.Width = 1000;
            chartForm.Height = 600;

            // Создаем и настраиваем Chart
            Chart chart = new Chart();
            chart.Dock = DockStyle.Fill;

            // Настройка области диаграммы
            ChartArea area = new ChartArea("MainArea");
            area.AxisX.Title = "Клиенты";
            area.AxisY.Title = "Сумма (руб)";
            chart.ChartAreas.Add(area);

            // Серия для сумм заказов
            Series ordersSeries = new Series("Сумма заказа");
            ordersSeries.ChartType = SeriesChartType.Column;
            ordersSeries.Color = Color.Blue;
            ordersSeries.IsValueShownAsLabel = true;

            // Серия для сумм доставок
            Series deliveriesSeries = new Series("Сумма доставки");
            deliveriesSeries.ChartType = SeriesChartType.Column;
            deliveriesSeries.Color = Color.Orange;
            deliveriesSeries.IsValueShownAsLabel = true;

            // Заполняем данными
            foreach (DataRow row in data.Rows)
            {
                string clientName = row["client_name"].ToString();
                decimal orderSum = Convert.ToDecimal(row["total_price"]);
                decimal deliverySum = Convert.ToDecimal(row["delivery_sum"]);

                ordersSeries.Points.AddXY(clientName, orderSum);
                deliveriesSeries.Points.AddXY(clientName, deliverySum);
            }

            chart.Series.Add(ordersSeries);
            chart.Series.Add(deliveriesSeries);

            // Настройка легенды
            Legend legend = new Legend();
            chart.Legends.Add(legend);

            // Заголовок диаграммы
            Title title = new Title("Соотношение сумм заказов и доставок по клиентам");
            chart.Titles.Add(title);

            chartForm.Controls.Add(chart);
            chartForm.ShowDialog();
        }

        private DataTable GetOrderDeliveryData(List<string> clientNames, DateTime startDate, DateTime endDate)
        {
            DataTable dt = new DataTable();

            string sql = @"
        SELECT 
            c.name as client_name,
            SUM(o.total_price) as total_price,
            SUM(CASE WHEN op.isDelivered THEN op.price * op.quantity ELSE 0 END) as delivery_sum
        FROM 
            Orders o
        JOIN 
            Clients c ON o.client_id = c.id
        JOIN 
            Orders_Products op ON o.id = op.order_id
        WHERE 
            c.name IN (" + string.Join(",", clientNames.Select(n => $"'{n.Replace("'", "''")}'")) + @")
            AND o.date BETWEEN @startDate AND @endDate
        GROUP BY 
            c.name
        ORDER BY 
            c.name";

            using (var cmd = new NpgsqlCommand(sql, con))
            {
                cmd.Parameters.AddWithValue("@startDate", startDate);
                cmd.Parameters.AddWithValue("@endDate", endDate);

                NpgsqlDataAdapter da = new NpgsqlDataAdapter(cmd);
                da.Fill(dt);
            }

            return dt;
        }

        private void buttonNo_Click(object sender, EventArgs e)
        {
            Close();
        }

        private void LoadClients()
        {
            try
            {
                checkedListBox1.Items.Clear();

                string sql = "SELECT name FROM Clients ORDER BY name";

                using (var cmd = new NpgsqlCommand(sql, con))
                using (var reader = cmd.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        checkedListBox1.Items.Add(reader.GetString(0).ToString());
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка при загрузке клиентов: {ex.Message}", "Ошибка",
                                MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
