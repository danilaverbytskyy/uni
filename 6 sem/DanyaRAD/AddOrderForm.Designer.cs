namespace DanyaRAD2
{
    partial class AddOrderForm
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
            components = new System.ComponentModel.Container();
            buttonNo = new Button();
            buttonYes = new Button();
            label2 = new Label();
            label1 = new Label();
            labelClients = new Label();
            label3 = new Label();
            contextMenuStrip1 = new ContextMenuStrip(components);
            label4 = new Label();
            dateTimePicker = new DateTimePicker();
            comboBoxClient = new ComboBox();
            totalPriceLabel = new Label();
            SuspendLayout();
            // 
            // buttonNo
            // 
            buttonNo.BackColor = Color.FromArgb(255, 128, 128);
            buttonNo.Font = new Font("Segoe UI", 12F);
            buttonNo.Location = new Point(257, 283);
            buttonNo.Name = "buttonNo";
            buttonNo.Size = new Size(118, 46);
            buttonNo.TabIndex = 28;
            buttonNo.Text = "Отмена";
            buttonNo.UseVisualStyleBackColor = false;
            buttonNo.Click += No_Click;
            // 
            // buttonYes
            // 
            buttonYes.BackColor = Color.Lime;
            buttonYes.Font = new Font("Segoe UI", 12F);
            buttonYes.Location = new Point(133, 283);
            buttonYes.Name = "buttonYes";
            buttonYes.Size = new Size(118, 46);
            buttonYes.TabIndex = 27;
            buttonYes.Text = "Добавить";
            buttonYes.UseVisualStyleBackColor = false;
            buttonYes.Click += Yes_Click;
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Font = new Font("Segoe UI", 12F);
            label2.Location = new Point(3, 197);
            label2.Name = "label2";
            label2.Size = new Size(58, 28);
            label2.TabIndex = 26;
            label2.Text = "Дата:";
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Font = new Font("Segoe UI", 12F);
            label1.Location = new Point(3, 154);
            label1.Name = "label1";
            label1.Size = new Size(81, 28);
            label1.TabIndex = 24;
            label1.Text = "Клиент:";
            // 
            // labelClients
            // 
            labelClients.AutoSize = true;
            labelClients.Font = new Font("Showcard Gothic", 18F, FontStyle.Regular, GraphicsUnit.Point, 0);
            labelClients.Location = new Point(94, 82);
            labelClients.Name = "labelClients";
            labelClients.Size = new Size(205, 37);
            labelClients.TabIndex = 22;
            labelClients.Text = "Новый Заказ";
            // 
            // label3
            // 
            label3.AutoSize = true;
            label3.Font = new Font("Segoe UI", 12F);
            label3.Location = new Point(3, 234);
            label3.Name = "label3";
            label3.Size = new Size(134, 28);
            label3.TabIndex = 29;
            label3.Text = "Полная цена:";
            // 
            // contextMenuStrip1
            // 
            contextMenuStrip1.ImageScalingSize = new Size(20, 20);
            contextMenuStrip1.Name = "contextMenuStrip1";
            contextMenuStrip1.Size = new Size(61, 4);
            // 
            // label4
            // 
            label4.AutoSize = true;
            label4.Font = new Font("Segoe UI", 12F);
            label4.Location = new Point(166, 243);
            label4.Name = "label4";
            label4.Size = new Size(0, 28);
            label4.TabIndex = 30;
            // 
            // dateTimePicker
            // 
            dateTimePicker.Font = new Font("Segoe UI", 13F);
            dateTimePicker.Location = new Point(146, 191);
            dateTimePicker.Name = "dateTimePicker";
            dateTimePicker.Size = new Size(250, 36);
            dateTimePicker.TabIndex = 32;
            // 
            // comboBoxClient
            // 
            comboBoxClient.Font = new Font("Segoe UI", 12F);
            comboBoxClient.FormattingEnabled = true;
            comboBoxClient.Location = new Point(146, 148);
            comboBoxClient.Name = "comboBoxClient";
            comboBoxClient.Size = new Size(250, 36);
            comboBoxClient.TabIndex = 33;
            // 
            // totalPriceLabel
            // 
            totalPriceLabel.AutoSize = true;
            totalPriceLabel.Font = new Font("Segoe UI", 12F);
            totalPriceLabel.Location = new Point(146, 234);
            totalPriceLabel.Name = "totalPriceLabel";
            totalPriceLabel.Size = new Size(99, 28);
            totalPriceLabel.TabIndex = 34;
            totalPriceLabel.Text = ":totalPrice";
            // 
            // AddOrderForm
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(429, 391);
            Controls.Add(totalPriceLabel);
            Controls.Add(comboBoxClient);
            Controls.Add(dateTimePicker);
            Controls.Add(label4);
            Controls.Add(label3);
            Controls.Add(buttonNo);
            Controls.Add(buttonYes);
            Controls.Add(label2);
            Controls.Add(label1);
            Controls.Add(labelClients);
            Name = "AddOrderForm";
            Text = "AddOrderForm";
            Load += AddOrderForm_Load;
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Button buttonNo;
        private Button buttonYes;
        private Label label2;
        private Label label1;
        private Label labelClients;
        private Label label3;
        private ContextMenuStrip contextMenuStrip1;
        private Label label4;
        private DateTimePicker dateTimePicker;
        private ComboBox comboBoxClient;
        private Label totalPriceLabel;
    }
}