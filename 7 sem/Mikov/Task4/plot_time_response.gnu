set terminal pngcairo size 1200,800 enhanced font 'Arial,12'
set output 'time_response.png'
set xlabel 'Время'
set ylabel 'Значения'
set title 'Временные характеристики системы (a1=2.8, a2=0.3, ?=0)'
set grid
set key top right
plot 'time_response.txt' using 1:2 with lines title 'x(t) - состояние', \
     '' using 1:3 with lines title 'v(t) - скорость', \
     '' using 1:4 with lines title 'u(t) - управление'
