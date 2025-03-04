namespace DanyaRAD
{
    partial class Form1
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
            button1 = new Button();
            richTextBox1 = new RichTextBox();
            textBoxFIO = new TextBox();
            checkedListBoxSections = new CheckedListBox();
            comboBoxCity = new ComboBox();
            radioButtonMale = new RadioButton();
            radioButtonFemale = new RadioButton();
            SuspendLayout();
            // 
            // button1
            // 
            button1.Font = new Font("Segoe UI", 12F);
            button1.Location = new Point(95, 402);
            button1.Name = "button1";
            button1.Size = new Size(198, 68);
            button1.TabIndex = 0;
            button1.Text = "Отправить";
            button1.UseVisualStyleBackColor = true;
            button1.Click += button1_Click;
            // 
            // richTextBox1
            // 
            richTextBox1.Font = new Font("Segoe UI", 12F);
            richTextBox1.Location = new Point(380, 28);
            richTextBox1.Name = "richTextBox1";
            richTextBox1.Size = new Size(393, 442);
            richTextBox1.TabIndex = 1;
            richTextBox1.Text = "";
            // 
            // textBoxFIO
            // 
            textBoxFIO.AccessibleDescription = "";
            textBoxFIO.Font = new Font("Segoe UI", 12F);
            textBoxFIO.Location = new Point(95, 28);
            textBoxFIO.Name = "textBoxFIO";
            textBoxFIO.PlaceholderText = "ФИО";
            textBoxFIO.Size = new Size(198, 34);
            textBoxFIO.TabIndex = 2;
            textBoxFIO.Tag = "";
            textBoxFIO.TextChanged += textBoxFIO_TextChanged;
            // 
            // checkedListBoxSections
            // 
            checkedListBoxSections.BackColor = SystemColors.ButtonShadow;
            checkedListBoxSections.Font = new Font("Segoe UI", 12F);
            checkedListBoxSections.FormattingEnabled = true;
            checkedListBoxSections.Items.AddRange(new object[] { "Английский", "Французский", "Немецкий", "Новогреческий", "Испанский", "Польский" });
            checkedListBoxSections.Location = new Point(95, 205);
            checkedListBoxSections.Name = "checkedListBoxSections";
            checkedListBoxSections.Size = new Size(198, 178);
            checkedListBoxSections.TabIndex = 3;
            // 
            // comboBoxCity
            // 
            comboBoxCity.Font = new Font("Segoe UI", 12F);
            comboBoxCity.FormattingEnabled = true;
            comboBoxCity.Items.AddRange(new object[] { "Краснодар", "Липецк", "Майкоп", "Москва", "Сочи", "Фащёвка", "Феодосия" });
            comboBoxCity.Location = new Point(95, 78);
            comboBoxCity.Name = "comboBoxCity";
            comboBoxCity.Size = new Size(198, 36);
            comboBoxCity.Sorted = true;
            comboBoxCity.TabIndex = 4;
            // 
            // radioButtonMale
            // 
            radioButtonMale.AutoSize = true;
            radioButtonMale.Font = new Font("Segoe UI", 12F);
            radioButtonMale.Location = new Point(95, 129);
            radioButtonMale.Name = "radioButtonMale";
            radioButtonMale.Size = new Size(115, 32);
            radioButtonMale.TabIndex = 5;
            radioButtonMale.TabStop = true;
            radioButtonMale.Text = "мужской";
            radioButtonMale.UseVisualStyleBackColor = true;
            radioButtonMale.CheckedChanged += radioButtonMale_CheckedChanged;
            // 
            // radioButtonFemale
            // 
            radioButtonFemale.AutoSize = true;
            radioButtonFemale.Font = new Font("Segoe UI", 12F);
            radioButtonFemale.Location = new Point(180, 167);
            radioButtonFemale.Name = "radioButtonFemale";
            radioButtonFemale.Size = new Size(113, 32);
            radioButtonFemale.TabIndex = 6;
            radioButtonFemale.TabStop = true;
            radioButtonFemale.Text = "женский";
            radioButtonFemale.UseVisualStyleBackColor = true;
            radioButtonFemale.CheckedChanged += radioButtonFemale_CheckedChanged;
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = SystemColors.ActiveCaption;
            ClientSize = new Size(811, 497);
            Controls.Add(radioButtonFemale);
            Controls.Add(radioButtonMale);
            Controls.Add(comboBoxCity);
            Controls.Add(checkedListBoxSections);
            Controls.Add(textBoxFIO);
            Controls.Add(richTextBox1);
            Controls.Add(button1);
            Name = "Form1";
            Text = "Form1";
            Load += Form1_Load;
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Button button1;
        private RichTextBox richTextBox1;
        private TextBox textBoxFIO;
        private CheckedListBox checkedListBoxSections;
        private ComboBox comboBoxCity;
        private RadioButton radioButtonMale;
        private RadioButton radioButtonFemale;
    }
}
