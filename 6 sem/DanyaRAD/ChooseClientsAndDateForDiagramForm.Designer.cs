namespace DanyaRAD2
{
    partial class ChooseClientsAndDateForDiagramForm
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
            dateTimePickerRightBorder = new DateTimePicker();
            label1 = new Label();
            labelClients = new Label();
            dateTimePickerLeftBorder = new DateTimePicker();
            checkedListBox1 = new CheckedListBox();
            SuspendLayout();
            // 
            // buttonNo
            // 
            buttonNo.BackColor = Color.FromArgb(255, 128, 128);
            buttonNo.Font = new Font("Segoe UI", 12F);
            buttonNo.Location = new Point(266, 448);
            buttonNo.Name = "buttonNo";
            buttonNo.Size = new Size(118, 46);
            buttonNo.TabIndex = 30;
            buttonNo.Text = "Отмена";
            buttonNo.UseVisualStyleBackColor = false;
            buttonNo.Click += buttonNo_Click;
            // 
            // buttonYes
            // 
            buttonYes.BackColor = Color.Lime;
            buttonYes.Font = new Font("Segoe UI", 12F);
            buttonYes.Location = new Point(105, 448);
            buttonYes.Name = "buttonYes";
            buttonYes.Size = new Size(163, 46);
            buttonYes.TabIndex = 29;
            buttonYes.Text = "Сформировать";
            buttonYes.UseVisualStyleBackColor = false;
            buttonYes.Click += buttonYes_Click;
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Font = new Font("Segoe UI", 12F);
            label2.Location = new Point(35, 179);
            label2.Name = "label2";
            label2.Size = new Size(38, 28);
            label2.TabIndex = 28;
            label2.Text = "По";
            // 
            // dateTimePickerRightBorder
            // 
            dateTimePickerRightBorder.CalendarFont = new Font("Segoe UI", 12F);
            dateTimePickerRightBorder.Font = new Font("Segoe UI", 12F);
            dateTimePickerRightBorder.Location = new Point(105, 179);
            dateTimePickerRightBorder.Name = "dateTimePickerRightBorder";
            dateTimePickerRightBorder.Size = new Size(276, 34);
            dateTimePickerRightBorder.TabIndex = 27;
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Font = new Font("Segoe UI", 12F);
            label1.Location = new Point(35, 129);
            label1.Name = "label1";
            label1.Size = new Size(24, 28);
            label1.TabIndex = 26;
            label1.Text = "С";
            // 
            // labelClients
            // 
            labelClients.AutoSize = true;
            labelClients.Font = new Font("Showcard Gothic", 18F, FontStyle.Regular, GraphicsUnit.Point, 0);
            labelClients.Location = new Point(35, 62);
            labelClients.Name = "labelClients";
            labelClients.Size = new Size(374, 37);
            labelClients.TabIndex = 25;
            labelClients.Text = "Построение диаграммы";
            // 
            // dateTimePickerLeftBorder
            // 
            dateTimePickerLeftBorder.CalendarFont = new Font("Segoe UI", 12F);
            dateTimePickerLeftBorder.Font = new Font("Segoe UI", 12F);
            dateTimePickerLeftBorder.Location = new Point(105, 129);
            dateTimePickerLeftBorder.Name = "dateTimePickerLeftBorder";
            dateTimePickerLeftBorder.Size = new Size(276, 34);
            dateTimePickerLeftBorder.TabIndex = 24;
            // 
            // checkedListBox1
            // 
            checkedListBox1.FormattingEnabled = true;
            checkedListBox1.Location = new Point(105, 235);
            checkedListBox1.Name = "checkedListBox1";
            checkedListBox1.Size = new Size(276, 202);
            checkedListBox1.TabIndex = 31;
            // 
            // ChooseClientsAndDateForDiagramForm
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(500, 506);
            Controls.Add(checkedListBox1);
            Controls.Add(buttonNo);
            Controls.Add(buttonYes);
            Controls.Add(label2);
            Controls.Add(dateTimePickerRightBorder);
            Controls.Add(label1);
            Controls.Add(labelClients);
            Controls.Add(dateTimePickerLeftBorder);
            Name = "ChooseClientsAndDateForDiagramForm";
            Text = "ChooseClientsAndDateForDiagramForm";
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Button buttonNo;
        private Button buttonYes;
        private Label label2;
        private DateTimePicker dateTimePickerRightBorder;
        private Label label1;
        private Label labelClients;
        private DateTimePicker dateTimePickerLeftBorder;
        private CheckedListBox checkedListBox1;
    }
}