using System;
using System.Windows.Markup;
using static System.Math;

namespace _35_2_Verbytskyy_Danila.NeuroNet
{
    class Neiron
    {
        private NeuronType type;//тип нейрона
        private double[] _weights;//его веса
        private double[] _inputs;//его входы
        private double _output;//его выход
        private double _derivative;//производная функции активации гипербтангенс
        private double a = 0.01;
        //входной 2 скрытых выходной    
        
        public double[] Weights { get => _weights; set => _weights = value; }
        public double[] Inputs
        {
            get { return _inputs; }
            set { _inputs = value; }
        }
        public double Output { get => _output; }
        public double Derivative { get => _derivative; }

        //конструктор
        public Neiron(double[] weights, NeuronType type)
        {
            this.type = type;
            _weights = weights;
        }

        

        public void Activator(double[] i, double[] w) //нелинейные преобразования
        {
            double sum = w[0]; //
            for (int m = 0; m < i.Length; m++)
                sum += i[m] * w[m + 1]; // Линейная комбинация входов и весов


            switch (type)
            {
                case NeuronType.Hidden:
                    _output = HyperbolicTan(sum); // Гиперболический тангенс
                    _derivative = HyperbolicTan_Derivator(sum);
                    break;
                case NeuronType.Output:
                    _output=Exp(sum);
                    break;
            }
        }



        private double HyperbolicTan(double sum)
        {
            double s= Exp(2 * sum);
            return (s-1) / (s+1);
        }
        private double HyperbolicTan_Derivator(double sum)
        {
            double d=HyperbolicTan(sum);
            return 1-d*d;
        }
    }
}
