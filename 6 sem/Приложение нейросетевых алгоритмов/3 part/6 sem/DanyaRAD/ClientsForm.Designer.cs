

namespace DanyaRAD2
{
    partial class ClientsForm
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
            menuBasic = new MenuStrip();
            addToolStripMenuItem = new ToolStripMenuItem();
            editToolStripMenuItem = new ToolStripMenuItem();
            deleteToolStripMenuItem = new ToolStripMenuItem();
            exitToolStripMenuItem = new ToolStripMenuItem();
            dataGridView1 = new DataGridView();
            labelClients = new Label();
            buttonCreateDiagram = new Button();
            menuBasic.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)dataGridView1).BeginInit();
            SuspendLayout();
            // 
            // menuBasic
            // 
            menuBasic.Font = new Font("Segoe UI", 12F);
            menuBasic.ImageScalingSize = new Size(20, 20);
            menuBasic.Items.AddRange(new ToolStripItem[] { addToolStripMenuItem, editToolStripMenuItem, deleteToolStripMenuItem, exitToolStripMenuItem });
            menuBasic.Location = new Point(0, 0);
            menuBasic.Name = "menuBasic";
            menuBasic.Size = new Size(947, 36);
            menuBasic.TabIndex = 1;
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
            // dataGridView1
            // 
            dataGridView1.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            dataGridView1.Location = new Point(32, 98);
            dataGridView1.Name = "dataGridView1";
            dataGridView1.RowHeadersWidth = 51;
            dataGridView1.Size = new Size(740, 313);
            dataGridView1.TabIndex = 2;
            // 
            // labelClients
            // 
            labelClients.AutoSize = true;
            labelClients.Font = new Font("Showcard Gothic", 18F, FontStyle.Regular, GraphicsUnit.Point, 0);
            labelClients.Location = new Point(335, 48);
            labelClients.Name = "labelClients";
            labelClients.Size = new Size(144, 37);
            labelClients.TabIndex = 3;
            labelClients.Text = "Клиенты";
            // 
            // buttonCreateDiagram
            // 
            buttonCreateDiagram.Font = new Font("Segoe UI", 12F);
            buttonCreateDiagram.Location = new Point(787, 301);
            buttonCreateDiagram.Name = "buttonCreateDiagram";
            buttonCreateDiagram.Size = new Size(132, 110);
            buttonCreateDiagram.TabIndex = 7;
            buttonCreateDiagram.Text = "Создать диаграмму клиентов";
            buttonCreateDiagram.UseVisualStyleBackColor = true;
            buttonCreateDiagram.Click += buttonCreateDiagram_Click;
            // 
            // ClientsForm
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(947, 439);
            Controls.Add(buttonCreateDiagram);
            Controls.Add(labelClients);
            Controls.Add(dataGridView1);
            Controls.Add(menuBasic);
            MainMenuStrip = menuBasic;
            Name = "ClientsForm";
            Text = "Clients";
            Load += Form2_Load;
            menuBasic.ResumeLayout(false);
            menuBasic.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)dataGridView1).EndInit();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion
        private MenuStrip menuBasic;
        private ToolStripMenuItem addToolStripMenuItem;
        private ToolStripMenuItem editToolStripMenuItem;
        private ToolStripMenuItem deleteToolStripMenuItem;
        private ToolStripMenuItem exitToolStripMenuItem;
        private DataGridView dataGridView1;
        private Label labelClients;
        private Button buttonCreateDiagram;
    }
}