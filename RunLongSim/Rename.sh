prefix="FileList"
file="gm2tracker_particle_gun_full.root"

for i in {0..15}; do

	echo $prefix$i

	echo $file

	echo gm2tracker_particle_gun_full_${i}.root

	cd $prefix$i

	mv $file gm2tracker_particle_gun_full_${i}.root

	#ls gm2tracker_particle_gun_full_${i}.root > ../FileList4HADD

	cd ../

done