﻿using System;
using System.Collections.Generic;
using System.IO;


namespace _35_2_Verbytskyy_P1.NeuroNet
{
    abstract class Layer
    {
        protected string name_Layer;
        string pathDirWeights;
        string pathFileWeights;
        protected int numofneurons;
        protected int numofprevneurons;
        protected const double learningrate = 0.005d; //скорость обучения
        protected const double momentum = 0.05; //param optimization 
        protected double[,] lastdeltaweights;
        Neuron[] _neurons;

        public Neuron[] Neurons { get => _neurons; set => _neurons = value; }

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
        //constructor
        protected Layer(int non, int nonp, NeuronType nt, string nm_Layer)
        {
            numofneurons = non;
            numofprevneurons = nonp;
            Neurons = new Neuron[non];
            name_Layer = nm_Layer;
            pathDirWeights = AppDomain.CurrentDomain.BaseDirectory + "memory\\"; // path to catalog
            pathFileWeights = pathDirWeights + name_Layer + "_memory.csv"; //path to file with synaptics weights
            double[,] Weights;
            if (File.Exists(pathFileWeights))
            {
                Weights = WeightInitialize(MemoryMode.GET, pathFileWeights);
            }
            else
            {
                Directory.CreateDirectory(pathDirWeights);
                Weights = WeightInitialize(MemoryMode.INIT, pathFileWeights);
            }

            lastdeltaweights = new double[non, nonp + 1];
            for (int i = 0; i < non; i++)
            {
                double[] tmp_weights = new double[nonp + 1];
                for (int j = 0; j < nonp + 1; j++)
                {
                    tmp_weights[j] = Weights[i, j];
                }
                Neurons[i] = new Neuron(tmp_weights, nt);
            }
        }

        public double[,] WeightInitialize(MemoryMode mm, string path)
        {
            int i, j;
            char[] delim = new char[] { ';', ' ' };
            string tmpStr;
            string[] tmpStrWeights;
            double[,] weights = new double[numofneurons, numofprevneurons + 1];

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

                case MemoryMode.INIT:
                    for (i = 0; i < numofneurons; i++)
                    {
                        double sum = 0;
                        double sumSquares = 0;

                        for (j = 0; j < numofprevneurons + 1; j++)
                        {
                            Random rand = new Random();
                            double randomWeight = (rand.NextDouble() * 2 - 1); // значение в диапазоне (-1; 1)
                            sum += weights[i, j];
                            sumSquares += weights[i, j] * weights[i, j];
                        }

                        double mean = sum / (numofprevneurons + 1);
                        double stdDev = Math.Sqrt(sumSquares / (numofprevneurons + 1));

                        for (j = 0; j < numofprevneurons + 1; j++)
                        {
                            weights[i, j] = (weights[i, j] - mean) / stdDev; //нормализация весов
                        }
                    }

                    WeightInitialize(MemoryMode.SET, path); //сохранение нормализованных весов в файл
                    break;
            }
            return weights;
        }
        //для прямых проходов
        abstract public void Recognize(Network net, Layer nextLayer);
        //для обратных проходов
        abstract public double[] BackwardPass(double[] stuff);
    }//прописать инициализацию и сохранение! 
     //Архитектура 15-70-31-10
}
