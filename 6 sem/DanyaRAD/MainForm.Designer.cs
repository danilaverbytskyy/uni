namespace DanyaRAD2
{
    partial class MainForm
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
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
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            buttonOrders = new Button();
            label1 = new Label();
            buttonProducts = new Button();
            buttonClients = new Button();
            SuspendLayout();
            // 
            // buttonOrders
            // 
            buttonOrders.Font = new Font("Segoe UI", 16F);
            buttonOrders.Location = new Point(140, 151);
            buttonOrders.Name = "buttonOrders";
            buttonOrders.Size = new Size(132, 77);
            buttonOrders.TabIndex = 0;
            buttonOrders.Text = "Заказы";
            buttonOrders.UseVisualStyleBackColor = true;
            buttonOrders.Click += buttonOrders_Click;
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Font = new Font("Showcard Gothic", 18F, FontStyle.Regular, GraphicsUnit.Point, 0);
            label1.Location = new Point(244, 48);
            label1.Name = "label1";
            label1.Size = new Size(284, 37);
            label1.TabIndex = 1;
            label1.Text = "Интернет Магазин";
            // 
            // buttonProducts
            // 
            buttonProducts.Font = new Font("Segoe UI", 16F);
            buttonProducts.Location = new Point(324, 151);
            buttonProducts.Name = "buttonProducts";
            buttonProducts.Size = new Size(132, 77);
            buttonProducts.TabIndex = 2;
            buttonProducts.Text = "Товары";
            buttonProducts.UseVisualStyleBackColor = true;
            buttonProducts.Click += buttonProducts_Click;
            // 
            // buttonClients
            // 
            buttonClients.Font = new Font("Segoe UI", 16F);
            buttonClients.Location = new Point(500, 151);
            buttonClients.Name = "buttonClients";
            buttonClients.Size = new Size(132, 77);
            buttonClients.TabIndex = 4;
            buttonClients.Text = "Клиенты";
            buttonClients.UseVisualStyleBackColor = true;
            buttonClients.Click += ButtonClients_Click;
            // 
            // MainForm
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.RosyBrown;
            ClientSize = new Size(799, 350);
            Controls.Add(buttonClients);
            Controls.Add(buttonProducts);
            Controls.Add(label1);
            Controls.Add(buttonOrders);
            Name = "MainForm";
            Text = "MainForm";
            Load += Form1_Load;
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Button buttonOrders;
        private Label label1;
        private Button buttonProducts;
        private Button buttonClients;
    }
}
