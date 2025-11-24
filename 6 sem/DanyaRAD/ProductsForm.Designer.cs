namespace DanyaRAD2
{
    partial class ProductsForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            labelClients = new Label();
            dataGridView1 = new DataGridView();
            menuBasic = new MenuStrip();
            addToolStripMenuItem = new ToolStripMenuItem();
            editToolStripMenuItem = new ToolStripMenuItem();
            deleteToolStripMenuItem = new ToolStripMenuItem();
            exitToolStripMenuItem = new ToolStripMenuItem();
            buttonFormReport = new Button();
            ((System.ComponentModel.ISupportInitialize)dataGridView1).BeginInit();
            menuBasic.SuspendLayout();
            SuspendLayout();
            // 
            // labelClients
            // 
            labelClients.AutoSize = true;
            labelClients.Font = new Font("Showcard Gothic", 18F, FontStyle.Regular, GraphicsUnit.Point, 0);
            labelClients.Location = new Point(332, 56);
            labelClients.Name = "labelClients";
            labelClients.Size = new Size(125, 37);
            labelClients.TabIndex = 6;
            labelClients.Text = "Товары";
            // 
            // dataGridView1
            // 
            dataGridView1.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            dataGridView1.Location = new Point(32, 96);
            dataGridView1.Name = "dataGridView1";
            dataGridView1.RowHeadersWidth = 51;
            dataGridView1.Size = new Size(740, 335);
            dataGridView1.TabIndex = 5;
            // 
            // menuBasic
            // 
            menuBasic.Font = new Font("Segoe UI", 12F);
            menuBasic.ImageScalingSize = new Size(20, 20);
            menuBasic.Items.AddRange(new ToolStripItem[] { addToolStripMenuItem, editToolStripMenuItem, deleteToolStripMenuItem, exitToolStripMenuItem });
            menuBasic.Location = new Point(0, 0);
            menuBasic.Name = "menuBasic";
            menuBasic.Size = new Size(961, 36);
            menuBasic.TabIndex = 4;
            menuBasic.Text = "menuStrip1";
            // 
            // addToolStripMenuItem
            // 
            addToolStripMenuItem.Name = "addToolStripMenuItem";
            addToolStripMenuItem.Size = new Size(115, 32);
            addToolStripMenuItem.Text = "Добавить";
            addToolStripMenuItem.Click += addToolStripMenuItem_Click;
            // 
            // editToolStripMenuItem
            // 
            editToolStripMenuItem.Name = "editToolStripMenuItem";
            editToolStripMenuItem.Size = new Size(116, 32);
            editToolStripMenuItem.Text = "Изменить";
            editToolStripMenuItem.Click += editToolStripMenuItem_Click;
            // 
            // deleteToolStripMenuItem
            // 
            deleteToolStripMenuItem.Name = "deleteToolStripMenuItem";
            deleteToolStripMenuItem.Size = new Size(99, 32);
            deleteToolStripMenuItem.Text = "Удалить";
            deleteToolStripMenuItem.Click += deleteToolStripMenuItem_Click;
            // 
            // exitToolStripMenuItem
            // 
            exitToolStripMenuItem.Name = "exitToolStripMenuItem";
            exitToolStripMenuItem.Size = new Size(83, 32);
            exitToolStripMenuItem.Text = "Выход";
            exitToolStripMenuItem.Click += exitToolStripMenuItem_Click;
            // 
            // buttonFormReport
            // 
            buttonFormReport.Font = new Font("Segoe UI", 12F);
            buttonFormReport.Location = new Point(801, 321);
            buttonFormReport.Name = "buttonFormReport";
            buttonFormReport.Size = new Size(132, 110);
            buttonFormReport.TabIndex = 7;
            buttonFormReport.Text = "Сформировать отчет по товарам";
            buttonFormReport.UseVisualStyleBackColor = true;
            buttonFormReport.Click += buttonFormReport_Click;
            // 
            // ProductsForm
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.LightGray;
            ClientSize = new Size(961, 460);
            Controls.Add(buttonFormReport);
            Controls.Add(labelClients);
            Controls.Add(dataGridView1);
            Controls.Add(menuBasic);
            Name = "ProductsForm";
            Text = "Products";
            ((System.ComponentModel.ISupportInitialize)dataGridView1).EndInit();
            menuBasic.ResumeLayout(false);
            menuBasic.PerformLayout();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Label labelClients;
        private DataGridView dataGridView1;
        private MenuStrip menuBasic;
        private ToolStripMenuItem addToolStripMenuItem;
        private ToolStripMenuItem editToolStripMenuItem;
        private ToolStripMenuItem deleteToolStripMenuItem;
        private ToolStripMenuItem exitToolStripMenuItem;
        private Button buttonFormReport;
    }
}