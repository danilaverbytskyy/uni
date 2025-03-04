using System;
using System.Collections.Generic;
using System.IO;
using System.Windows.Forms;

namespace _35_2_Verbytskyy_Danila.NeuroNet
{
    abstract class Layer
    {
        protected string name_Layer;
        string pathDirWeights;
        string pathFileWeights;
        protected int numofneurons;
        protected int numofprevneurons;
        protected const double learningrate = 0.001;
        protected const double momentum = 0.9;
        protected double[,] lastdeltaweights;
        protected Neiron[] neurons;

        //svoistva
        public Neiron[] Neurons { get => neurons; set => neurons = value; }

        public double[] Data
        {
            set
            {
                for (int i = 0; i < Neurons.Length; i++)
                {
                    Neurons[i].Inputs = value;
                    Neurons[i].Activator(Neurons[i].Inputs, Neurons[i].Weights);
                }
            }
        }
        //konstruktor
        protected Layer(int non,int nopn,NeuronType nt,string nm_Layer)
        {
            int i, j;
            numofneurons = non;
            numofprevneurons = nopn;
            Neurons = new Neiron[non];
            name_Layer = nm_Layer;
            pathDirWeights = AppDomain.CurrentDomain.BaseDirectory + "memory\\";
            pathFileWeights = pathDirWeights + name_Layer + "_memory.csv";//put k failu sinapt vesov
            double[,] Weights;
            if (File.Exists(pathFileWeights))
            {
                Weights = WeightInitialize(MemoryMode.GET, pathFileWeights);
            }
            else
            {
                Directory.CreateDirectory(pathDirWeights);
                Weights=WeightInitialize(MemoryMode.INIT, pathFileWeights);
            }
            lastdeltaweights = new double[non, nopn + 1];

            for (i = 0; i < non; i++)
            {
                double[] tmp_weights = new double[nopn + 1];
                for (j = 0; j < nopn + 1; j++)
                {
                    tmp_weights[j]=Weights[i,j];

                }
                Neurons[i] = new Neiron(tmp_weights, nt);
            }
        }
        public double[,] WeightInitialize(MemoryMode mm, string path, double[,] weights = null)
        {
            int i, j;
            char[] delim = new char[] { ';', ' ' };
            string tmpStr;
            string[] tmpStrWeights;


            if (weights == null)
                weights = new double[numofneurons, numofprevneurons + 1];

            switch (mm)
            {
                case MemoryMode.GET:
                    tmpStrWeights = File.ReadAllLines(path);
                    string[] memory_element;
                    for (i = 0; i < numofneurons; i++)
                    {
                        memory_element = tmpStrWeights[i].Split(delim);
                        for (j = 0; j < numofprevneurons + 1; j++)
                        {
                            weights[i, j] = double.Parse(memory_element[j].Replace(',', '.'), System.Globalization.CultureInfo.InvariantCulture);
                        }
                    }
                    break;

                case MemoryMode.INIT:
                    Random rand = new Random(); // Инициализация один раз

                    for (i = 0; i < numofneurons; i++)
                    {
                        double sum = 0;
                        double sumSquares = 0;

                        for (j = 0; j < numofprevneurons + 1; j++)
                        {
                            double randomWeight = (rand.NextDouble() * 2 - 1); // значение в диапазоне (-1; 1)
                            weights[i, j] = randomWeight;
                            sum += weights[i, j];
                            sumSquares += weights[i, j] * weights[i, j];
                        }

                        double mean = sum / (numofprevneurons + 1);
                        double stdDev = Math.Sqrt(sumSquares / (numofprevneurons + 1));

                        for (j = 0; j < numofprevneurons + 1; j++)
                        {
                            double s = (weights[i, j] - mean) / stdDev;
                            weights[i, j] = s; //нормализация весов
                            if (weights[i, j] > 1) weights[i, j] = 1;
                            if (weights[i, j] < -1) weights[i, j] = -1;
                        }
                    }

                    // Сохранение нормализованных весов в файл
                    WeightInitialize(MemoryMode.SET, path, weights);
                    break;

                case MemoryMode.SET:
                    List<string> lines = new List<string>();

                    for (i = 0; i < numofneurons; i++)
                    {
                        string line = "";
                        for (j = 0; j < numofprevneurons + 1; j++)
                        {
                            line += weights[i, j].ToString(System.Globalization.CultureInfo.InvariantCulture) + ";";
                        }
                        lines.Add(line.TrimEnd(';'));
                    }

                    File.WriteAllLines(path, lines);
                    break;
            }

            return weights;
        }
        abstract public void Recognize(NetWork net, Layer nextLayer);
        abstract public double[] BackwardPass(double[] stuff);
    }
}
