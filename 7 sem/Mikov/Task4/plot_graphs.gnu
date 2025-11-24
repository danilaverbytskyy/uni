set terminal pngcairo size 1000,800 enhanced font 'Arial,12'
set output 'critical_tau_graph.png'
set xlabel 'Параметр a1'
set ylabel 'Критическое запаздывание ?'
set title 'Критические значения параметров устойчивости'
set grid
set key top right
plot \
     'critical_tau_a2_0.1.txt' with linespoints title 'a2=0.1', \
     'critical_tau_a2_0.2.txt' with linespoints title 'a2=0.2', \
     'critical_tau_a2_0.3.txt' with linespoints title 'a2=0.3', \
     'critical_tau_a2_0.4.txt' with linespoints title 'a2=0.4', \
     'critical_tau_a2_0.5.txt' with linespoints title 'a2=0.5'
