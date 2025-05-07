namespace DanyaRAD2
{
    partial class AddClientForm
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
            textName = new TextBox();
            label1 = new Label();
            label2 = new Label();
            textAddress = new TextBox();
            label3 = new Label();
            textPhone = new TextBox();
            buttonYes = new Button();
            buttonNo = new Button();
            SuspendLayout();
            // 
            // labelClients
            // 
            labelClients.AutoSize = true;
            labelClients.Font = new Font("Showcard Gothic", 18F, FontStyle.Regular, GraphicsUnit.Point, 0);
            labelClients.Location = new Point(72, 24);
            labelClients.Name = "labelClients";
            labelClients.Size = new Size(223, 37);
            labelClients.TabIndex = 4;
            labelClients.Text = "Новый Клиент";
            // 
            // textName
            // 
            textName.Font = new Font("Segoe UI", 12F);
            textName.Location = new Point(111, 87);
            textName.Name = "textName";
            textName.Size = new Size(267, 34);
            textName.TabIndex = 5;
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Font = new Font("Segoe UI", 12F);
            label1.Location = new Point(12, 87);
            label1.Name = "label1";
            label1.Size = new Size(55, 28);
            label1.TabIndex = 6;
            label1.Text = "Имя:";
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Font = new Font("Segoe UI", 12F);
            label2.Location = new Point(12, 133);
            label2.Name = "label2";
            label2.Size = new Size(71, 28);
            label2.TabIndex = 8;
            label2.Text = "Адрес:";
            // 
            // textAddress
            // 
            textAddress.Font = new Font("Segoe UI", 12F);
            textAddress.Location = new Point(111, 130);
            textAddress.Name = "textAddress";
            textAddress.Size = new Size(267, 34);
            textAddress.TabIndex = 7;
            // 
            // label3
            // 
            label3.AutoSize = true;
            label3.Font = new Font("Segoe UI", 12F);
            label3.Location = new Point(12, 173);
            label3.Name = "label3";
            label3.Size = new Size(95, 28);
            label3.TabIndex = 10;
            label3.Text = "Телефон:";
            // 
            // textPhone
            // 
            textPhone.Font = new Font("Segoe UI", 12F);
            textPhone.Location = new Point(111, 170);
            textPhone.Name = "textPhone";
            textPhone.Size = new Size(267, 34);
            textPhone.TabIndex = 9;
            // 
            // buttonYes
            // 
            buttonYes.BackColor = Color.Lime;
            buttonYes.Font = new Font("Segoe UI", 12F);
            buttonYes.Location = new Point(111, 230);
            buttonYes.Name = "buttonYes";
            buttonYes.Size = new Size(118, 46);
            buttonYes.TabIndex = 11;
            buttonYes.Text = "Добавить";
            buttonYes.UseVisualStyleBackColor = false;
            buttonYes.Click += Yes_Click;
            // 
            // buttonNo
            // 
            buttonNo.BackColor = Color.FromArgb(255, 128, 128);
            buttonNo.Font = new Font("Segoe UI", 12F);
            buttonNo.Location = new Point(235, 230);
            buttonNo.Name = "buttonNo";
            buttonNo.Size = new Size(118, 46);
            buttonNo.TabIndex = 12;
            buttonNo.Text = "Отмена";
            buttonNo.UseVisualStyleBackColor = false;
            buttonNo.Click += No_Click;
            // 
            // AddClientForm
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(390, 326);
            Controls.Add(buttonNo);
            Controls.Add(buttonYes);
            Controls.Add(label3);
            Controls.Add(textPhone);
            Controls.Add(label2);
            Controls.Add(textAddress);
            Controls.Add(label1);
            Controls.Add(textName);
            Controls.Add(labelClients);
            Name = "AddClientForm";
            Text = "AddClientForm";
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Label labelClients;
        private TextBox textName;
        private Label label1;
        private Label label2;
        private TextBox textAddress;
        private Label label3;
        private TextBox textPhone;
        private Button buttonYes;
        private Button buttonNo;
    }
}