# Define output path
#path=/gm2/app/users/sgrant/Offline/LowDCAs/JobOutput/

#returnPath=/gm2/app/users/sgrant/Offline/LowDCAs/

# If STOP file is created, pause job
if [ -f STOP ]; then 
  echo "STOP file found. Not processing"
  return
  exit
fi

# Label piped input file
inFile=$1
echo $inFile

# Check if it's output already exists
#if [ -d $inFile ]; then
#  echo "$inFile already exists..."
#  return
#  exit
#fi

# If not, create a new dir for output, copy input file into it
mkdir $inFile
cd $inFile
cp ../Files/$inFile .

# Get the list of root files
filesToRun=""
for line in `cat $inFile`; do
  filesToRun=$filesToRun" "$line
done

# Run sim
echo $filesToRun
gm2 -c /gm2/app/users/sgrant/Offline/LowDCAs/fcl/RunSimLongScan.fcl -s $filesToRun
#gm2 -c /gm2/app/users/sgrant/Offline/LowDCAs/FCL/RunSimLowDCAs500.fcl -S $inFile
# -T TrackCaloMatchingSim_${inFile}.root
# Return to run dir
cd ../

# Run sim
# gm2 -c /gm2/app/users/sgrant/Offline/LowDCAs/FCL/RunSimLowDCAs500.fcl -S $inFile