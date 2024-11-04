using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;
using System.Windows.Forms.VisualStyles;
using System.Web;

namespace _35_2_Verbytskyy_P1
{
    public partial class Form1 : Form
    {
        private double[] _inputPixels = new double[15] { 0d, 0d, 0d, 0d, 0d, 0d, 0d, 0d, 0d, 0d, 0d, 0d, 0d, 0d, 0d };
        private NeuroNet.Network net = new NeuroNet.Network();

        public Form1()
        {
            InitializeComponent();
        }

        private void ChangeState(Button b, int index)
        {
            if (b.BackColor == Color.Green)
            {
                b.BackColor = Color.White;
                _inputPixels[index] = 0d;
            }
            else if (b.BackColor == Color.White)
            {
                b.BackColor = Color.Green;
                _inputPixels[index] = 1d;
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            ChangeState(button1, 0);
            button1.Text = _inputPixels[0].ToString();
        }
        

        private void button2_Click(object sender, EventArgs e)
        {
            ChangeState(button2, 1);
            button2.Text = _inputPixels[1].ToString();
        }

        private void button3_Click(object sender, EventArgs e)
        {
            ChangeState(button3, 2);
            button3.Text = _inputPixels[2].ToString();
        }

        private void button4_Click(object sender, EventArgs e)
        {
            ChangeState(button4, 3);
            button4.Text = _inputPixels[3].ToString();
        }

        private void button5_Click(object sender, EventArgs e)
        {
            ChangeState(button5, 4);
            button5.Text = _inputPixels[4].ToString();
        }

        private void button6_Click(object sender, EventArgs e)
        {
            ChangeState(button6, 5);
            button6.Text = _inputPixels[5].ToString();
        }

        private void button7_Click(object sender, EventArgs e)
        {
            ChangeState(button7, 6);
            button7.Text = _inputPixels[6].ToString();
        }

        private void button8_Click(object sender, EventArgs e)
        {
            ChangeState(button8, 7);
            button8.Text = _inputPixels[7].ToString();
        }

        private void button9_Click(object sender, EventArgs e)
        {
            ChangeState(button9, 8);
            button9.Text = _inputPixels[8].ToString();
        }

        private void button10_Click(object sender, EventArgs e)
        {
            ChangeState(button10, 9);
            button10.Text = _inputPixels[9].ToString();
        }

        private void button11_Click(object sender, EventArgs e)
        {
            ChangeState(button11, 10);
            button11.Text = _inputPixels[10].ToString();
        }

        private void button12_Click(object sender, EventArgs e)
        {
            ChangeState(button12, 11);
            button12.Text = _inputPixels[11].ToString();
        }

        private void button13_Click(object sender, EventArgs e)
        {
            ChangeState(button13, 12);
            button13.Text = _inputPixels[12].ToString();
        }

        private void button14_Click(object sender, EventArgs e)
        {
            ChangeState(button14, 13);
            button14.Text = _inputPixels[13].ToString();
        }

        private void button15_Click(object sender, EventArgs e)
        {
            ChangeState(button15, 14);
            button15.Text = _inputPixels[14].ToString();
        }

        private void numericUpDown1_ValueChanged(object sender, EventArgs e)
        {

        }

        private void buttonSaveTrainSample_Click(object sender, EventArgs e)
        {
            SaveTrain(numericUpDownAnswer.Value, _inputPixels);
        }

        private void SaveTrain(decimal value, double[]input)
        {
            string pathDir = AppDomain.CurrentDomain.BaseDirectory;
            string nameFileTrain = pathDir + "train.txt";

            string numberCombination = value.ToString() + " ";
            for (int i = 0; i < input.Length; i++)
            {
                numberCombination += input[i].ToString();
            }

            numberCombination += "\n";
            if (File.Exists(nameFileTrain))
            {
                File.AppendAllText(nameFileTrain, numberCombination);
            }
        }

        private void buttonSaveTestSample_Click(object sender, EventArgs e)
        {
            SaveTest(numericUpDownAnswer.Value, _inputPixels);
        }

        private void SaveTest(decimal value, double[] input)
        {
            string pathDir = AppDomain.CurrentDomain.BaseDirectory;
            string nameFileTest = pathDir + "test.txt";

            string numberCombination = value.ToString() + " ";
            for (int i = 0; i < input.Length; i++)
            {
                numberCombination += input[i].ToString();
            }

            numberCombination += "\n";
            if (File.Exists(nameFileTest))
            {
                File.AppendAllText(nameFileTest, numberCombination);
            }
        }

        private void buttonRecognize_Click(object sender, EventArgs e)
        {
            net.ForwardPass(net, _inputPixels);
            labelFact.Text = net.fact.ToList().IndexOf(net.fact.Max()).ToString();
        }
    }
}
