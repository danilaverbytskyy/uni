using System;
using System.CodeDom.Compiler;
using System.IO;

namespace _35_2_Verbytskyy_Danila.NeuroNet
{
    internal class InputLayer { 
        private Random random = new Random();

        private double[,] trainset = new double[100, 16];
        private double[,] testset = new double[10, 16];
        public double[,] Trainset { get=>trainset;}
        public double[,] Testset { get=>testset;}
        public InputLayer(NetworkMode nm)
        {
            string path = AppDomain.CurrentDomain.BaseDirectory;
            string[] tmpStr;
            string[] tmpArrStr;
            double[] tmpArr;
            

            switch (nm)
            {
                case NetworkMode.Train:
                    tmpArrStr = File.ReadAllLines(path + "train.txt");
                    for (int i = 0; i < tmpArrStr.Length; i++)
                    {
                        
                        string example = tmpArrStr[i];
                        if (example.Length == 16) 
                        {
                            
                            trainset[i, 0] = double.Parse(example[0].ToString(), System.Globalization.CultureInfo.InvariantCulture);
                            
                            for (int j = 1; j < 16; j++)
                            {
                                trainset[i, j] = double.Parse(example[j].ToString(), System.Globalization.CultureInfo.InvariantCulture);
                            }
                        }
                    }

                    
                    Shuffling_Array_Rows(trainset);
                    break;

                case NetworkMode.Test:
                    tmpArrStr = File.ReadAllLines(path + "test.txt");
                    for (int i = 0; i < tmpArrStr.Length; i++)
                    {
                        string example = tmpArrStr[i];
                        if (example.Length == 16) 
                        {
                            
                            testset[i, 0] = double.Parse(example[0].ToString(), System.Globalization.CultureInfo.InvariantCulture);
                            
                            for (int j = 1; j < 16; j++)
                            {
                                testset[i, j] = double.Parse(example[j].ToString(), System.Globalization.CultureInfo.InvariantCulture);
                            }
                        }
                    }
                    break;

                case NetworkMode.Recogn:
                    break;
            }
        }
        public void Shuffling_Array_Rows(double[,] arr)
        {
            int j;
            Random random= new Random();
            double[]temp=new double[arr.GetLength(1)];
            for (int n = trainset.GetLength(0) - 1; n >= 1; n--)
            {
                
                j = random.Next(n + 1);
                for (int i = 0; i < arr.GetLength(1); i++)
                {

                    temp[i] = arr[n, i];
                }
                for (int i = 0; i < arr.GetLength(1); i++)
                {
                    arr[n, i] = arr[j, i];
                    arr[j, i] = temp[i];
                }
            }
        }

    }
}
