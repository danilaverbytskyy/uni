using System;

namespace _35_2_Verbytskyy_Danila.NeuroNet
{
    class NetWork
    {
        //15 70 32 10 verbytskyy
        private InputLayer input_layer = null;
        private HiddenLayer hidden_layer1 = new HiddenLayer(70, 15, NeuronType.Hidden, nameof(hidden_layer1));
        private HiddenLayer hidden_layer2 = new HiddenLayer(32, 70, NeuronType.Hidden, nameof(hidden_layer2));
        private OutputLayer output_layer = new OutputLayer(10, 32, NeuronType.Output, nameof(output_layer));

        public double[] fact = new double[10];
        private double[] e_error_avr;

        public double[] E_error_avr { get => e_error_avr; set => e_error_avr = value; }


        public NetWork() { }
        
        public void Train(NetWork net)
        {
            int epoches = 40;
            net.input_layer = new InputLayer(NetworkMode.Train);
            double tmpSumError;
            double[] errors;
            double[] temp_grsums1;
            double[] temp_grsums2;

            e_error_avr = new double[epoches];

            for (int k = 0; k < epoches; k++) // перебор эпох обучения
            {
                e_error_avr[k] = 0;
                net.input_layer.Shuffling_Array_Rows(net.input_layer.Trainset);
                for (int i = 0; i < net.input_layer.Trainset.GetLength(0); i++)
                {
                    double[] tmpTrain = new double[15];
                    for (int j = 0; j < tmpTrain.Length; j++)
                    {
                        tmpTrain[j] = net.input_layer.Trainset[i, j + 1];
                    }

                    ForwardPass(net, tmpTrain);
                    tmpSumError = 0;
                    errors = new double[net.fact.Length];
                    for (int x = 0; x < errors.Length; x++)
                    {
                        if (x == net.input_layer.Trainset[i, 0])
                            errors[x] = 1 - net.fact[x];
                        else errors[x] = -net.fact[x];

                        tmpSumError += errors[x] * errors[x] / 2;
                    }

                    e_error_avr[k] += tmpSumError / errors.Length;//zyfch elem massiva
                    temp_grsums2 = net.output_layer.BackwardPass(errors);
                    temp_grsums1 = net.hidden_layer2.BackwardPass(temp_grsums2);
                    net.hidden_layer1.BackwardPass(temp_grsums1);
                }

                e_error_avr[k] /= net.input_layer.Trainset.GetLength(0);
            }

            net.input_layer = null; // завершение обучения, данные больше не нужны

            // Сохранение весов в файлы
            SaveWeights();
        }

        private void SaveWeights()
        {
            string pathBase = AppDomain.CurrentDomain.BaseDirectory + "memory\\";
            hidden_layer1.WeightInitialize(MemoryMode.SET, pathBase + "hidden_layer1_memory.csv", GetWeights(hidden_layer1));
            hidden_layer2.WeightInitialize(MemoryMode.SET, pathBase + "hidden_layer2_memory.csv", GetWeights(hidden_layer2));
            output_layer.WeightInitialize(MemoryMode.SET, pathBase + "output_layer_memory.csv", GetWeights(output_layer));
        }

        private double[,] GetWeights(Layer layer)
        {
            double[,] weights = new double[layer.Neurons.Length, layer.Neurons[0].Weights.Length];

            for (int i = 0; i < layer.Neurons.Length; i++)
            {
                for (int j = 0; j < layer.Neurons[i].Weights.Length; j++)
                {
                    weights[i, j] = layer.Neurons[i].Weights[j];
                }
            }

            return weights;
        }

        public void ForwardPass(NetWork net, double[] netInput)
        {
            net.hidden_layer1.Data = netInput;
            net.hidden_layer1.Recognize(null, net.hidden_layer2);
            net.hidden_layer2.Recognize(null, net.output_layer);
            net.output_layer.Recognize(net, null);
        }
        public void Test(NetWork net) {
            int epoches = 3;
            net.input_layer = new InputLayer(NetworkMode.Test);
            double tmpSumError;
            double[] errors;

            e_error_avr = new double[epoches];

            for (int k = 0; k < epoches; k++) // перебор эпох обучения
            {
                e_error_avr[k] = 0;
                
                for (int i = 0; i < net.input_layer.Testset.GetLength(0); i++)
                {
                    double[] tmpTest = new double[15];
                    for (int j = 0; j < tmpTest.Length; j++)
                    {
                        tmpTest[j] = net.input_layer.Testset[i, j + 1];
                    }

                    ForwardPass(net, tmpTest);
                    tmpSumError = 0;
                    errors = new double[net.fact.Length];
                    for (int x = 0; x < errors.Length; x++)
                    {
                        if (x == net.input_layer.Testset[i, 0])
                            errors[x] = 1 - net.fact[x];
                        else errors[x] = -net.fact[x];

                        tmpSumError += errors[x] * errors[x] / 2;
                    }

                    e_error_avr[k] += tmpSumError / errors.Length;//zyfch elem massiva
                    
                }

                e_error_avr[k] /= net.input_layer.Testset.GetLength(0);
            }

            net.input_layer = null; // завершение обучения, данные больше не нужны

        }
    }
}
