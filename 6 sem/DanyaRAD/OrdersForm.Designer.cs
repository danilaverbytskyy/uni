namespace DanyaRAD2
{
    partial class OrdersForm
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
            заказToolStripMenuItem = new ToolStripMenuItem();
            содержимоеToolStripMenuItem = new ToolStripMenuItem();
            editToolStripMenuItem = new ToolStripMenuItem();
            заказToolStripMenuItem1 = new ToolStripMenuItem();
            deleteToolStripMenuItem = new ToolStripMenuItem();
            заказToolStripMenuItem2 = new ToolStripMenuItem();
            содержимоеToolStripMenuItem1 = new ToolStripMenuItem();
            exitToolStripMenuItem = new ToolStripMenuItem();
            label1 = new Label();
            dataGridView2 = new DataGridView();
            button1 = new Button();
            изменитьДоставленностьToolStripMenuItem = new ToolStripMenuItem();
            ((System.ComponentModel.ISupportInitialize)dataGridView1).BeginInit();
            menuBasic.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)dataGridView2).BeginInit();
            SuspendLayout();
            // 
            // labelClients
            // 
            labelClients.AutoSize = true;
            labelClients.Font = new Font("Showcard Gothic", 18F, FontStyle.Regular, GraphicsUnit.Point, 0);
            labelClients.Location = new Point(198, 66);
            labelClients.Name = "labelClients";
            labelClients.Size = new Size(126, 37);
            labelClients.TabIndex = 9;
            labelClients.Text = "Заказы";
            // 
            // dataGridView1
            // 
            dataGridView1.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            dataGridView1.Location = new Point(32, 106);
            dataGridView1.Name = "dataGridView1";
            dataGridView1.RowHeadersWidth = 51;
            dataGridView1.Size = new Size(573, 567);
            dataGridView1.TabIndex = 8;
            dataGridView1.CellClick += dataGridView1_CellClick;
            // 
            // menuBasic
            // 
            menuBasic.Font = new Font("Segoe UI", 12F);
            menuBasic.ImageScalingSize = new Size(20, 20);
            menuBasic.Items.AddRange(new ToolStripItem[] { addToolStripMenuItem, editToolStripMenuItem, deleteToolStripMenuItem, exitToolStripMenuItem });
            menuBasic.Location = new Point(0, 0);
            menuBasic.Name = "menuBasic";
            menuBasic.Size = new Size(1291, 36);
            menuBasic.TabIndex = 7;
            menuBasic.Text = "menuStrip1";
            // 
            // addToolStripMenuItem
            // 
            addToolStripMenuItem.DropDownItems.AddRange(new ToolStripItem[] { заказToolStripMenuItem, содержимоеToolStripMenuItem });
            addToolStripMenuItem.Name = "addToolStripMenuItem";
            addToolStripMenuItem.Size = new Size(115, 32);
            addToolStripMenuItem.Text = "Добавить";
            // 
            // заказToolStripMenuItem
            // 
            заказToolStripMenuItem.Name = "заказToolStripMenuItem";
            заказToolStripMenuItem.Size = new Size(218, 32);
            заказToolStripMenuItem.Text = "Заказ";
            заказToolStripMenuItem.Click += addToolStripMenuItem_Click;
            // 
            // содержимоеToolStripMenuItem
            // 
            содержимоеToolStripMenuItem.Name = "содержимоеToolStripMenuItem";
            содержимоеToolStripMenuItem.Size = new Size(218, 32);
            содержимоеToolStripMenuItem.Text = "Содержимое";
            содержимоеToolStripMenuItem.Click += contentToolStripMenuItem_Click_Add;
            // 
            // editToolStripMenuItem
            // 
            editToolStripMenuItem.DropDownItems.AddRange(new ToolStripItem[] { заказToolStripMenuItem1, изменитьДоставленностьToolStripMenuItem });
            editToolStripMenuItem.Name = "editToolStripMenuItem";
            editToolStripMenuItem.Size = new Size(116, 32);
            editToolStripMenuItem.Text = "Изменить";
            // 
            // заказToolStripMenuItem1
            // 
            заказToolStripMenuItem1.Name = "заказToolStripMenuItem1";
            заказToolStripMenuItem1.Size = new Size(338, 32);
            заказToolStripMenuItem1.Text = "Заказ";
            заказToolStripMenuItem1.Click += editToolStripMenuItem_Click;
            // 
            // deleteToolStripMenuItem
            // 
            deleteToolStripMenuItem.DropDownItems.AddRange(new ToolStripItem[] { заказToolStripMenuItem2, содержимоеToolStripMenuItem1 });
            deleteToolStripMenuItem.Name = "deleteToolStripMenuItem";
            deleteToolStripMenuItem.Size = new Size(99, 32);
            deleteToolStripMenuItem.Text = "Удалить";
            // 
            // заказToolStripMenuItem2
            // 
            заказToolStripMenuItem2.Name = "заказToolStripMenuItem2";
            заказToolStripMenuItem2.Size = new Size(218, 32);
            заказToolStripMenuItem2.Text = "Заказ";
            заказToolStripMenuItem2.Click += deleteToolStripMenuItem_Click;
            // 
            // содержимоеToolStripMenuItem1
            // 
            содержимоеToolStripMenuItem1.Name = "содержимоеToolStripMenuItem1";
            содержимоеToolStripMenuItem1.Size = new Size(218, 32);
            содержимоеToolStripMenuItem1.Text = "Содержимое";
            содержимоеToolStripMenuItem1.Click += contentToolStripMenuItem1_Click_Delete;
            // 
            // exitToolStripMenuItem
            // 
            exitToolStripMenuItem.Name = "exitToolStripMenuItem";
            exitToolStripMenuItem.Size = new Size(83, 32);
            exitToolStripMenuItem.Text = "Выход";
            exitToolStripMenuItem.Click += exitToolStripMenuItem_Click;
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Font = new Font("Showcard Gothic", 18F, FontStyle.Regular, GraphicsUnit.Point, 0);
            label1.Location = new Point(830, 66);
            label1.Name = "label1";
            label1.Size = new Size(210, 37);
            label1.TabIndex = 11;
            label1.Text = "Содержимое";
            // 
            // dataGridView2
            // 
            dataGridView2.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            dataGridView2.Location = new Point(664, 106);
            dataGridView2.Name = "dataGridView2";
            dataGridView2.RowHeadersWidth = 51;
            dataGridView2.Size = new Size(573, 567);
            dataGridView2.TabIndex = 10;
            // 
            // button1
            // 
            button1.Font = new Font("Segoe UI", 12F);
            button1.Location = new Point(495, 52);
            button1.Name = "button1";
            button1.Size = new Size(273, 39);
            button1.TabIndex = 12;
            button1.Text = "Эксопорт  в MS Excel";
            button1.UseVisualStyleBackColor = true;
            button1.Click += buttonExportExcel_Click;
            // 
            // изменитьДоставленностьToolStripMenuItem
            // 
            изменитьДоставленностьToolStripMenuItem.Name = "изменитьДоставленностьToolStripMenuItem";
            изменитьДоставленностьToolStripMenuItem.Size = new Size(338, 32);
            изменитьДоставленностьToolStripMenuItem.Text = "Изменить доставленность";
            изменитьДоставленностьToolStripMenuItem.Click += изменитьДоставленностьToolStripMenuItem_Click;
            // 
            // OrdersForm
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(1291, 685);
            Controls.Add(button1);
            Controls.Add(label1);
            Controls.Add(dataGridView2);
            Controls.Add(labelClients);
            Controls.Add(dataGridView1);
            Controls.Add(menuBasic);
            Name = "OrdersForm";
            Text = "OrdersForm";
            Load += OrdersForm_Load;
            ((System.ComponentModel.ISupportInitialize)dataGridView1).EndInit();
            menuBasic.ResumeLayout(false);
            menuBasic.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)dataGridView2).EndInit();
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
        private Label label1;
        private DataGridView dataGridView2;
        private ToolStripMenuItem заказToolStripMenuItem;
        private ToolStripMenuItem содержимоеToolStripMenuItem;
        private ToolStripMenuItem заказToolStripMenuItem1;
        private ToolStripMenuItem заказToolStripMenuItem2;
        private ToolStripMenuItem содержимоеToolStripMenuItem1;
        private Button button1;
        private ToolStripMenuItem изменитьДоставленностьToolStripMenuItem;
    }
}