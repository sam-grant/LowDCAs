for i in {200..225}; do
#    mkdir Plots${i}
    cd Plots${i}
    gm2 -c ../../fcl/RunPlotsSimScan.fcl -s ../../RunSim/File${i}/gm2tracker_sim_scan.root
    cd ../
done

#hadd -f LowDCAs_SimScanPlotsFull_Ambiguous.root Plots*/LowDCAs_SimScanPlots.root