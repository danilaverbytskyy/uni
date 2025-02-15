using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace _35_2_Verbytskyy_P1.NeuroNet
{
    internal class InputLayer
    {
        private Random random = new Random();

        private double[,] trainset = new double[100, 16];
        private double[,] testset = new double[16, 10];

        public double[,] TrainSet { get => trainset; }

        public double[,] TestSet { get => testset; }

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
                        tmpStr = tmpArrStr[i].Split();
                        tmpArr = new double[tmpStr.Length];
                        for (int j = 0; j < tmpStr.Length; j++)
                        {
                            tmpArr[j] = double.Parse(tmpStr[j],
                                System.Globalization.CultureInfo.InvariantCulture);
                        }
                    }

                    for(int n=TrainSet.GetLength(0)-1; n>=1; n--)
                    {
                        int j = random.Next(n + 1);
                        double[] temp = new double[TrainSet.GetLength(1)];
                        for (int i = 0; i < TrainSet.GetLength(1); i++)
                        {
                            temp[i] = TrainSet[n, i];
                        }
                        for(int i=0; i < TrainSet.GetLength(1); i++)
                        {
                            trainset[n, i] = trainset[j, i];
                            trainset[j, i] = temp[i];
                        }
                        
                    }
                    break;

                case NetworkMode.Test:
                    tmpArrStr = File.ReadAllLines(path + "test.txt");
                    for (int i = 0; i < tmpArrStr.Length; i++)
                    {
                        tmpStr = tmpArrStr[i].Split();
                        for (int j = 0; j < tmpStr.Length; j++)
                        {
                            testset[i, j] = double.Parse(tmpStr[j], System.Globalization.CultureInfo.InvariantCulture);
                        }
                    }
                    break;

                case NetworkMode.Recogn:
                    break;
            }
        }

        public void Shuffling_Array_Rows(double[,] arr)
        {
            int j; // номер случайно выбранной строки
            Random random = new Random();
            double[] temp = new double[arr.GetLength(1)]; //вспомогательный массив

            for(int n=arr.GetLength(0) - 1; n >= 1; n--) //цикл перебора строк снизу вверх
            {
                j = random.Next(n + 1); //выбор случайной строки из выше расположенных строк

                for(int i=0; i < arr.GetLength(1); i++) // цикл копирования n-ой строки
                {
                    temp[i] = arr[n, i];
                }
                for(int i=0; i<arr.GetLength(1); i++) //цикл перестановки двух строк
                {
                    arr[n, i] = arr[j, i];
                    arr[j, i] = temp[i];
                }
            }
        }
    }
}
