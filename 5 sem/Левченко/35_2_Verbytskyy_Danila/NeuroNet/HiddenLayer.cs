

namespace _35_2_Verbytskyy_Danila.NeuroNet
{
    class HiddenLayer : Layer
    {
        public HiddenLayer(int non,int nopn,NeuronType nt,string type):
            base(non, nopn, nt, type) { }

        public override void Recognize(NetWork net, Layer nextLayer)
        {
            double[] hidden_out=new double[Neurons.Length];
            for (int i=0; i<Neurons.Length; i++)
                hidden_out[i]=Neurons[i].Output;
            nextLayer.Data = hidden_out;
        }
        public override double[] BackwardPass(double[] gr_sums)
        {
            double[] gr_sum=new double[numofprevneurons];
            for (int j = 0; j < numofprevneurons; j++)
            {
                double sum = 0;
                for (int k = 0; k < numofneurons; k++)
                {
                    sum += neurons[k].Weights[j] * neurons[k].Derivative * gr_sums[k];
                }
                gr_sum[j] = sum;
            }
            
            for (int i = 0; i < numofneurons; i++)
            {
                for (int n = 0; n < numofprevneurons + 1; n++)
                {
                    double deltaw;
                    if (n == 0)
                    {
                        deltaw=momentum*lastdeltaweights[i,0]+learningrate*neurons[i].Derivative*gr_sums[i];
                    }
                    else
                    {
                        deltaw = momentum * lastdeltaweights[i, n] + learningrate * neurons[i].Inputs[n - 1] * neurons[i].Derivative * gr_sums[i];
                    }
                    lastdeltaweights[i,n] = deltaw;
                    neurons[i].Weights[n] += deltaw;

                }
            }
            return gr_sum;
        }
    }
}
