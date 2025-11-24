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
    public partial class ChooseDateForProductsReportForm : Form
    {
        NpgsqlConnection con;
        int id;
        public bool IsReportCreated { get; private set; }
        public DateTime leftBorderDate { get; private set; }
        public DateTime rightBorderDate { get; private set; }
        public ChooseDateForProductsReportForm(NpgsqlConnection con)
        {
            InitializeComponent();
            this.con = con;
        }

        private void buttonNo_Click(object sender, EventArgs e)
        {
            Close();
        }

        private void buttonYes_Click(object sender, EventArgs e)
        {
            leftBorderDate = dateTimePickerLeftBorder.Value;
            rightBorderDate = dateTimePickerRightBorder.Value;
            IsReportCreated = true;
            Close();
        }
    }
}
