namespace DanyaRAD2
{
    partial class AddContentOrderForm
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
            OrderIdLabel = new Label();
            comboBoxProducts = new ComboBox();
            label4 = new Label();
            label3 = new Label();
            buttonNo = new Button();
            buttonYes = new Button();
            label1 = new Label();
            labelClients = new Label();
            label2 = new Label();
            textBoxPrice = new TextBox();
            textBoxQuantity = new TextBox();
            label5 = new Label();
            checkBoxDelivered = new CheckBox();
            SuspendLayout();
            // 
            // OrderIdLabel
            // 
            OrderIdLabel.AutoSize = true;
            OrderIdLabel.Font = new Font("Segoe UI", 12F);
            OrderIdLabel.Location = new Point(76, 99);
            OrderIdLabel.Name = "OrderIdLabel";
            OrderIdLabel.Size = new Size(89, 28);
            OrderIdLabel.TabIndex = 44;
            OrderIdLabel.Text = ":order_id";
            // 
            // comboBoxProducts
            // 
            comboBoxProducts.Font = new Font("Segoe UI", 12F);
            comboBoxProducts.FormattingEnabled = true;
            comboBoxProducts.Location = new Point(150, 139);
            comboBoxProducts.Name = "comboBoxProducts";
            comboBoxProducts.Size = new Size(246, 36);
            comboBoxProducts.TabIndex = 43;
            // 
            // label4
            // 
            label4.AutoSize = true;
            label4.Font = new Font("Segoe UI", 12F);
            label4.Location = new Point(171, 108);
            label4.Name = "label4";
            label4.Size = new Size(0, 28);
            label4.TabIndex = 41;
            // 
            // label3
            // 
            label3.AutoSize = true;
            label3.Font = new Font("Segoe UI", 12F);
            label3.Location = new Point(12, 99);
            label3.Name = "label3";
            label3.Size = new Size(74, 28);
            label3.TabIndex = 40;
            label3.Text = "Заказ#";
            // 
            // buttonNo
            // 
            buttonNo.BackColor = Color.FromArgb(255, 128, 128);
            buttonNo.Font = new Font("Segoe UI", 12F);
            buttonNo.Location = new Point(278, 315);
            buttonNo.Name = "buttonNo";
            buttonNo.Size = new Size(118, 46);
            buttonNo.TabIndex = 39;
            buttonNo.Text = "Отмена";
            buttonNo.UseVisualStyleBackColor = false;
            buttonNo.Click += buttonNo_Click;
            // 
            // buttonYes
            // 
            buttonYes.BackColor = Color.Lime;
            buttonYes.Font = new Font("Segoe UI", 12F);
            buttonYes.Location = new Point(150, 315);
            buttonYes.Name = "buttonYes";
            buttonYes.Size = new Size(118, 46);
            buttonYes.TabIndex = 38;
            buttonYes.Text = "Добавить";
            buttonYes.UseVisualStyleBackColor = false;
            buttonYes.Click += buttonYes_Click;
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Font = new Font("Segoe UI", 12F);
            label1.Location = new Point(12, 142);
            label1.Name = "label1";
            label1.Size = new Size(71, 28);
            label1.TabIndex = 36;
            label1.Text = "Товар:";
            // 
            // labelClients
            // 
            labelClients.AutoSize = true;
            labelClients.Font = new Font("Showcard Gothic", 18F, FontStyle.Regular, GraphicsUnit.Point, 0);
            labelClients.Location = new Point(21, 46);
            labelClients.Name = "labelClients";
            labelClients.Size = new Size(359, 37);
            labelClients.TabIndex = 35;
            labelClients.Text = "Добавить товар в заказ";
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Font = new Font("Segoe UI", 12F);
            label2.Location = new Point(12, 189);
            label2.Name = "label2";
            label2.Size = new Size(63, 28);
            label2.TabIndex = 45;
            label2.Text = "Цена:";
            // 
            // textBoxPrice
            // 
            textBoxPrice.Font = new Font("Segoe UI", 12F);
            textBoxPrice.Location = new Point(150, 186);
            textBoxPrice.Name = "textBoxPrice";
            textBoxPrice.Size = new Size(246, 34);
            textBoxPrice.TabIndex = 46;
            // 
            // textBoxQuantity
            // 
            textBoxQuantity.Font = new Font("Segoe UI", 12F);
            textBoxQuantity.Location = new Point(150, 229);
            textBoxQuantity.Name = "textBoxQuantity";
            textBoxQuantity.Size = new Size(246, 34);
            textBoxQuantity.TabIndex = 48;
            // 
            // label5
            // 
            label5.AutoSize = true;
            label5.Font = new Font("Segoe UI", 12F);
            label5.Location = new Point(12, 229);
            label5.Name = "label5";
            label5.Size = new Size(124, 28);
            label5.TabIndex = 47;
            label5.Text = "Количество:";
            // 
            // checkBoxDelivered
            // 
            checkBoxDelivered.AutoSize = true;
            checkBoxDelivered.Font = new Font("Segoe UI", 12F);
            checkBoxDelivered.Location = new Point(150, 277);
            checkBoxDelivered.Name = "checkBoxDelivered";
            checkBoxDelivered.Size = new Size(131, 32);
            checkBoxDelivered.TabIndex = 50;
            checkBoxDelivered.Text = "Доставлен";
            checkBoxDelivered.UseVisualStyleBackColor = true;
            // 
            // AddContentOrderForm
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(408, 405);
            Controls.Add(checkBoxDelivered);
            Controls.Add(textBoxQuantity);
            Controls.Add(label5);
            Controls.Add(textBoxPrice);
            Controls.Add(label2);
            Controls.Add(OrderIdLabel);
            Controls.Add(comboBoxProducts);
            Controls.Add(label4);
            Controls.Add(label3);
            Controls.Add(buttonNo);
            Controls.Add(buttonYes);
            Controls.Add(label1);
            Controls.Add(labelClients);
            Name = "AddContentOrderForm";
            Text = "AddContentOrderForm";
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Label OrderIdLabel;
        private ComboBox comboBoxProducts;
        private Label label4;
        private Label label3;
        private Button buttonNo;
        private Button buttonYes;
        private Label label1;
        private Label labelClients;
        private Label label2;
        private TextBox textBoxPrice;
        private TextBox textBoxQuantity;
        private Label label5;
        private CheckBox checkBoxDelivered;
    }
}