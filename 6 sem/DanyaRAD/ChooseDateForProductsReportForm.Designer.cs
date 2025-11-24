namespace DanyaRAD2
{
    partial class ChooseDateForProductsReportForm
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
            dateTimePickerLeftBorder = new DateTimePicker();
            labelClients = new Label();
            label1 = new Label();
            label2 = new Label();
            dateTimePickerRightBorder = new DateTimePicker();
            buttonNo = new Button();
            buttonYes = new Button();
            SuspendLayout();
            // 
            // dateTimePickerLeftBorder
            // 
            dateTimePickerLeftBorder.CalendarFont = new Font("Segoe UI", 12F);
            dateTimePickerLeftBorder.Font = new Font("Segoe UI", 12F);
            dateTimePickerLeftBorder.Location = new Point(99, 88);
            dateTimePickerLeftBorder.Name = "dateTimePickerLeftBorder";
            dateTimePickerLeftBorder.Size = new Size(276, 34);
            dateTimePickerLeftBorder.TabIndex = 0;
            // 
            // labelClients
            // 
            labelClients.AutoSize = true;
            labelClients.Font = new Font("Showcard Gothic", 18F, FontStyle.Regular, GraphicsUnit.Point, 0);
            labelClients.Location = new Point(29, 21);
            labelClients.Name = "labelClients";
            labelClients.Size = new Size(346, 37);
            labelClients.TabIndex = 7;
            labelClients.Text = "Формирование отчета";
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Font = new Font("Segoe UI", 12F);
            label1.Location = new Point(29, 88);
            label1.Name = "label1";
            label1.Size = new Size(24, 28);
            label1.TabIndex = 8;
            label1.Text = "С";
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Font = new Font("Segoe UI", 12F);
            label2.Location = new Point(32, 154);
            label2.Name = "label2";
            label2.Size = new Size(38, 28);
            label2.TabIndex = 10;
            label2.Text = "По";
            // 
            // dateTimePickerRightBorder
            // 
            dateTimePickerRightBorder.CalendarFont = new Font("Segoe UI", 12F);
            dateTimePickerRightBorder.Font = new Font("Segoe UI", 12F);
            dateTimePickerRightBorder.Location = new Point(102, 154);
            dateTimePickerRightBorder.Name = "dateTimePickerRightBorder";
            dateTimePickerRightBorder.Size = new Size(276, 34);
            dateTimePickerRightBorder.TabIndex = 9;
            // 
            // buttonNo
            // 
            buttonNo.BackColor = Color.FromArgb(255, 128, 128);
            buttonNo.Font = new Font("Segoe UI", 12F);
            buttonNo.Location = new Point(260, 217);
            buttonNo.Name = "buttonNo";
            buttonNo.Size = new Size(118, 46);
            buttonNo.TabIndex = 23;
            buttonNo.Text = "Отмена";
            buttonNo.UseVisualStyleBackColor = false;
            buttonNo.Click += buttonNo_Click;
            // 
            // buttonYes
            // 
            buttonYes.BackColor = Color.Lime;
            buttonYes.Font = new Font("Segoe UI", 12F);
            buttonYes.Location = new Point(102, 217);
            buttonYes.Name = "buttonYes";
            buttonYes.Size = new Size(163, 46);
            buttonYes.TabIndex = 22;
            buttonYes.Text = "Сформировать";
            buttonYes.UseVisualStyleBackColor = false;
            buttonYes.Click += buttonYes_Click;
            // 
            // ChooseDateForProductsReportForm
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(410, 342);
            Controls.Add(buttonNo);
            Controls.Add(buttonYes);
            Controls.Add(label2);
            Controls.Add(dateTimePickerRightBorder);
            Controls.Add(label1);
            Controls.Add(labelClients);
            Controls.Add(dateTimePickerLeftBorder);
            Name = "ChooseDateForProductsReportForm";
            Text = "ChooseDateForProductsReportForm";
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private DateTimePicker dateTimePickerLeftBorder;
        private Label labelClients;
        private Label label1;
        private Label label2;
        private DateTimePicker dateTimePickerRightBorder;
        private Button buttonNo;
        private Button buttonYes;
    }
}