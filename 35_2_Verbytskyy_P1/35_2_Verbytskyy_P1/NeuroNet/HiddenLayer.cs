namespace _35_2_Verbytskyy_P1.NeuroNet
{
    class HiddenLayer : Layer
    {
        public HiddenLayer(int non, int nopn, NeuronType nt, string type) : 
            base(non, nopn, nt, type){ }

        public override void Recognize(Network net, Layer nextLayer)
        {
            double[] hidden_out = new double[Neurons.Length];

            for(int i = 0; i<Neurons.Length; i++)
            {
                hidden_out[i] = Neurons[i].Output;
            }
            nextLayer.Data = hidden_out;
        }

        public override double[] BackwardPass(double[] gr_sums)
        {
            double[] gr_sum = new double[numofneurons];
            //здесь код обучения нейросети
            return gr_sum;
        }
    }
}
