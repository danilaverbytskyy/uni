using System;
using System.IO;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace _35_2_Verbytskyy_Danila
{
    public partial class Form1 : Form
    {
        private NeuroNet.NetWork net=new NeuroNet.NetWork();
        private double[] inputPixels = new double[15] { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
        public Form1()
        {
            InitializeComponent();
        }

        private void ChangeState(Button b, int index)
        {
            if (b.BackColor == Color.Black)
            {
                b.BackColor = Color.White;
                b.ForeColor = Color.Black;
                inputPixels[index] = 0;
            }
            else if (b.BackColor == Color.White)
            {
                b.BackColor = Color.Black;
                b.ForeColor = Color.White;
                inputPixels[index] = 1;
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            ChangeState(button1, 0);
            button1.Text = inputPixels[0].ToString();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            ChangeState(button2, 1);
            button2.Text = inputPixels[1].ToString();
        }

        private void button3_Click(object sender, EventArgs e)
        {
            ChangeState(button3, 2);
            button3.Text = inputPixels[2].ToString();
        }

        private void button4_Click(object sender, EventArgs e)
        {
            ChangeState(button4, 3);
            button4.Text = inputPixels[3].ToString();
        }

        private void button5_Click(object sender, EventArgs e)
        {
            ChangeState(button5, 4);
            button5.Text = inputPixels[4].ToString();
        }

        private void button6_Click(object sender, EventArgs e)
        {
            ChangeState(button6, 5);
            button6.Text = inputPixels[5].ToString();
        }

        private void button7_Click(object sender, EventArgs e)
        {
            ChangeState(button7, 6);
            button7.Text = inputPixels[6].ToString();
        }

        private void button8_Click(object sender, EventArgs e)
        {
            ChangeState(button8, 7);
            button8.Text = inputPixels[7].ToString();
        }

        private void button9_Click(object sender, EventArgs e)
        {
            ChangeState(button9, 8);
            button9.Text = inputPixels[8].ToString();
        }

        private void button10_Click(object sender, EventArgs e)
        {
            ChangeState(button10, 9);
            button10.Text = inputPixels[9].ToString();
        }

        private void button11_Click(object sender, EventArgs e)
        {
            ChangeState(button11, 10);
            button11.Text = inputPixels[10].ToString();
        }

        private void button12_Click(object sender, EventArgs e)
        {
            ChangeState(button12, 11);
            button12.Text = inputPixels[11].ToString();
        }

        private void button13_Click(object sender, EventArgs e)
        {
            ChangeState(button13, 12);
            button13.Text = inputPixels[12].ToString();
        }

        private void button14_Click(object sender, EventArgs e)
        {
            ChangeState(button14, 13);
            button14.Text = inputPixels[13].ToString();
        }

        private void button15_Click(object sender, EventArgs e)
        {
            ChangeState(button15, 14);
            button15.Text = inputPixels[14].ToString();
        }

        private void numericUpDownOtvet_ValueChanged(object sender, EventArgs e)
        {

        }

        private void button_Teach_Click(object sender, EventArgs e)
        {
            SaveTrain(numericUpDownOtvet.Value, inputPixels);
        }

        private void button_Test_Click(object sender, EventArgs e)
        {
            SaveTest(numericUpDownOtvet.Value, inputPixels);
        }
        private void SaveTrain(decimal value,double[] input)
        {
            string pathDir;
            string nameFileTrain;
            pathDir = AppDomain.CurrentDomain.BaseDirectory;
            nameFileTrain = pathDir + "train.txt";
            string[] tmpStr = new string[1];
            tmpStr[0] = value.ToString();
            for (int i = 0; i < 15; i++)
            {
                tmpStr[0] += input[i].ToString();
            }
            File.AppendAllLines(nameFileTrain, tmpStr);
            

        }
        private void SaveTest(decimal value, double[] input)
        {
            string pathDir;
            string nameFileTest;
            pathDir = AppDomain.CurrentDomain.BaseDirectory;
            nameFileTest = pathDir + "test.txt";
            string[] tmpStr = new string[1];
            tmpStr[0] = value.ToString()+' ';
            for (int i = 0; i < 15; i++)
            {
                tmpStr[0] += input[i].ToString();
            }
            File.AppendAllLines(nameFileTest, tmpStr);


        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void button16_Click(object sender, EventArgs e)
        {
            net.ForwardPass(net, inputPixels);
            label1.Text=net.fact.ToList().IndexOf(net.fact.Max()).ToString();
            labelProbability.Text=(100*net.fact.Max()).ToString("0.00")+" %";
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void buttonTrain_Click(object sender, EventArgs e)
        {
            net.Train(net);
            for (int i = 0; i < net.E_error_avr.Length; i++)
            {
                charEavr.Series[0].Points.AddY(net.E_error_avr[i]);
            }
            MessageBox.Show("Обученик завершено","Информация",MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void label2_Click(object sender, EventArgs e)
        {

        }
        //testirovat
        private void buttonTest_Click(object sender, EventArgs e)
        {
            net.Test(net);
            for (int i = 0; i < net.E_error_avr.Length; i++)
            {
                charEavr.Series[0].Points.AddY(net.E_error_avr[i]);
            }
            MessageBox.Show("Тестирование завершено", "Информация", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }
    }
}
