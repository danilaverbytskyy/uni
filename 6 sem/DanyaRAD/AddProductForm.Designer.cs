namespace DanyaRAD2
{
    partial class AddProductForm
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
            buttonNo = new Button();
            buttonYes = new Button();
            label2 = new Label();
            textAddress = new TextBox();
            label1 = new Label();
            textName = new TextBox();
            labelClients = new Label();
            SuspendLayout();
            // 
            // buttonNo
            // 
            buttonNo.BackColor = Color.FromArgb(255, 128, 128);
            buttonNo.Font = new Font("Segoe UI", 12F);
            buttonNo.Location = new Point(238, 240);
            buttonNo.Name = "buttonNo";
            buttonNo.Size = new Size(118, 46);
            buttonNo.TabIndex = 21;
            buttonNo.Text = "Отмена";
            buttonNo.UseVisualStyleBackColor = false;
            buttonNo.Click += No_Click;
            // 
            // buttonYes
            // 
            buttonYes.BackColor = Color.Lime;
            buttonYes.Font = new Font("Segoe UI", 12F);
            buttonYes.Location = new Point(114, 240);
            buttonYes.Name = "buttonYes";
            buttonYes.Size = new Size(118, 46);
            buttonYes.TabIndex = 20;
            buttonYes.Text = "Добавить";
            buttonYes.UseVisualStyleBackColor = false;
            buttonYes.Click += Yes_Click;
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Font = new Font("Segoe UI", 12F);
            label2.Location = new Point(7, 169);
            label2.Name = "label2";
            label2.Size = new Size(80, 28);
            label2.TabIndex = 17;
            label2.Text = "Ед.изм.:";
            // 
            // textAddress
            // 
            textAddress.Font = new Font("Segoe UI", 12F);
            textAddress.Location = new Point(117, 166);
            textAddress.Name = "textAddress";
            textAddress.Size = new Size(267, 34);
            textAddress.TabIndex = 16;
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Font = new Font("Segoe UI", 12F);
            label1.Location = new Point(7, 126);
            label1.Name = "label1";
            label1.Size = new Size(104, 28);
            label1.TabIndex = 15;
            label1.Text = "Название:";
            // 
            // textName
            // 
            textName.Font = new Font("Segoe UI", 12F);
            textName.Location = new Point(117, 123);
            textName.Name = "textName";
            textName.Size = new Size(267, 34);
            textName.TabIndex = 14;
            // 
            // labelClients
            // 
            labelClients.AutoSize = true;
            labelClients.Font = new Font("Showcard Gothic", 18F, FontStyle.Regular, GraphicsUnit.Point, 0);
            labelClients.Location = new Point(75, 60);
            labelClients.Name = "labelClients";
            labelClients.Size = new Size(204, 37);
            labelClients.TabIndex = 13;
            labelClients.Text = "Новый Товар";
            // 
            // AddProductForm
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(396, 372);
            Controls.Add(buttonNo);
            Controls.Add(buttonYes);
            Controls.Add(label2);
            Controls.Add(textAddress);
            Controls.Add(label1);
            Controls.Add(textName);
            Controls.Add(labelClients);
            Name = "AddProductForm";
            Text = "AddProductForm";
            Load += AddProductForm_Load;
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Button buttonNo;
        private Button buttonYes;
        private Label label2;
        private TextBox textAddress;
        private Label label1;
        private TextBox textName;
        private Label labelClients;
    }
}