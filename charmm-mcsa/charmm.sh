for i in `seq 0 1 $2`;do
echo -n >/tmp/ahaile/$3/drude-current.p234.$1.$i.$4.mme
done

for i in `seq 0 1 $2`;do
/opt/mackerell/apps/charmm/serial/c42a2-serial   mme=/tmp/ahaile/$3/drude-current.p234.$1.$i.$4.mme q=p234 p=p2 run=$1 index=$i lb=$4 jobid=$3  -i /tmp/ahaile/$3/veri.inp234 > /tmp/ahaile/$3/dihedral.p2.$1.$i.out &
done
wait

for i in `seq 0 1 $2`;do
/opt/mackerell/apps/charmm/serial/c42a2-serial   mme=/tmp/ahaile/$3/drude-current.p234.$1.$i.$4.mme q=p234 p=p3 run=$1 index=$i lb=$4 jobid=$3  -i /tmp/ahaile/$3/veri.inp234 > /tmp/ahaile/$3/dihedral.p3.$1.$i.out &
done
wait

for i in `seq 0 1 $2`;do
/opt/mackerell/apps/charmm/serial/c42a2-serial   mme=/tmp/ahaile/$3/drude-current.p234.$1.$i.$4.mme q=p234 p=p4 run=$1 index=$i lb=$4 jobid=$3  -i /tmp/ahaile/$3/veri.inp234 > /tmp/ahaile/$3/dihedral.p4.$1.$i.out &
done
wait


for i in `seq 0 1 $2`;do
/opt/mackerell/apps/charmm/serial/c42a2-serial   mme=/tmp/ahaile/$3/drude-current.p234.$1.$i.$4.mme q=p234 p=p2n run=$1 index=$i lb=$4 jobid=$3  -i /tmp/ahaile/$3/veri.inp234 > /tmp/ahaile/$3/dihedral.p2.$1.$i.out &
done
wait

for i in `seq 0 1 $2`;do
/opt/mackerell/apps/charmm/serial/c42a2-serial   mme=/tmp/ahaile/$3/drude-current.p234.$1.$i.$4.mme q=p234 p=p3n run=$1 index=$i lb=$4 jobid=$3  -i /tmp/ahaile/$3/veri.inp234 > /tmp/ahaile/$3/dihedral.p3.$1.$i.out &
done
wait

for i in `seq 0 1 $2`;do
/opt/mackerell/apps/charmm/serial/c42a2-serial   mme=/tmp/ahaile/$3/drude-current.p234.$1.$i.$4.mme q=p234 p=p4n run=$1 index=$i lb=$4 jobid=$3  -i /tmp/ahaile/$3/veri.inp234 > /tmp/ahaile/$3/dihedral.p4.$1.$i.out &
done
wait

