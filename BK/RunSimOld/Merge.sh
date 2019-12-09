prefix="FileList"
file="gm2tracker_particle_gun_full.root"

for i in {0..15} ; do
    # if test -f "$prefix$i/$file"; then
    cd FileList$i
    	
	hadd -f "../gm2tracker_particle_gun_full_200.root" $file

	cd ../
#    fi
done



