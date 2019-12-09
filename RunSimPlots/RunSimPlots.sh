for i in {200..225}; do
    #mkdir Plots${i}
    cd Plots${i}
    gm2 -c ../FCL/RunPlotsSimLowDCAs500.fcl -s ../RunSim/File${i}/gm2tracker_particle_gun_full.root
    cd ../
done

hadd -f Plots/LowDCAsSimPlots500_MottTest.root Plots*/LowDCAsSimPlots500.root