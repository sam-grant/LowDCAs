path=/pnfs/GM2/mc/run1_gasgun_1062/runs_1567190000/1567190852

for i in {200..225}; do
    ls $path/gm2ringsim_muon_gasgun_truth_22551${i}_1567190852.1.root > Files/File${i}
done   

