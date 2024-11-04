namespace _35_2_Verbytskyy_P1.NeuroNet
{
    class OutputLayer : Layer
    {
        public OutputLayer(int non, int nopn, NeuronType nt, string type) :
            base(non, nopn, nt, type) { }

        public override void Recognize(Network net, Layer nextLayer)
        {
            double e_sum = 0;

            for (int i = 0; i < Neurons.Length; i++)
                e_sum += Neurons[i].Output;

            for(int i = 0;i < Neurons.Length;i++)
                net.fact[i] = Neurons[i].Output / e_sum;
        }

        public override double[] BackwardPass(double[] errors)
        {
            double[] gr_sum = new double[numofneurons + 1];
            //код обучения
            return gr_sum;
        }
    }
}
