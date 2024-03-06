for x in `seq 5 1 9`;do
for y in 1 2 ;do
pypy ./reweight.py ${z}e${x}e$y 0.0 <input.glycopeptidee >${y}$x.out &

done
wait
done

