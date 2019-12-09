for i in {200..225}; do
    mkdir Plots${i}
    cd Plots${i}
    gm2 -c ../../FCL/RunPlotsSimLowDCAs500.fcl -s ../../RunSimNoDrift/File${i}/gm2tracker_particle_gun_full.root
    cd ../
done

hadd -f Plots/LowDCAsSimPlots500All_NoDrift.root Plots*/LowDCAsSimPlots500.root