for i in {200..225}; do
#    mkdir Plots${i}
    cd Plots${i}
    gm2 -c ../../fcl/RunPlotsSimLongScan.fcl -s ../../RunLongSim/File${i}/gm2tracker_sim_scan.root
    cd ../
done

hadd -f LowDCAs_SimScanLongPlots_HitLevel.root Plots*/LowDCAs_SimLongScanPlots.root