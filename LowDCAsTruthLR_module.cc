// Contains LR truth information
// Sam Grant - Oct 2019

// Include needed ART headers
#include "art/Framework/Core/EDAnalyzer.h"
#include "art/Framework/Core/ModuleMacros.h"
#include "art/Framework/Principal/Event.h"
#include "art/Framework/Services/Optional/TFileService.h"
#include "art/Framework/Services/Registry/ServiceHandle.h"
#include "canvas/Persistency/Common/FindManyP.h"

//art records
#include "gm2dataproducts/strawtracker/StrawDigitArtRecord.hh"
#include "gm2dataproducts/strawtracker/StrawDCADigitArtRecord.hh"
#include "gm2dataproducts/strawtracker/StrawTimeIslandArtRecord.hh"
#include "gm2dataproducts/strawtracker/TrackCandidateArtRecord.hh"
#include "gm2dataproducts/strawtracker/TrackArtRecord.hh"
#include "gm2dataproducts/strawtracker/TrackDetailArtRecord.hh"
#include "gm2dataproducts/mc/ghostdetectors/GhostDetectorArtRecord.hh"

//Utils
#include "gm2geom/common/Gm2Constants_service.hh"
#include "gm2util/common/dataModuleDefs.hh"
#include "gm2util/common/RootManager.hh"
#include "gm2util/coordSystems/CoordSystemUtils.hh"
#include "gm2tracker/quality/TrackQuality_service.hh"
#include "gm2geom/strawtracker/StrawTrackerGeometry_service.hh"
#include "gm2tracker/utils/GeaneTrackUtils.hh"
#include "gm2tracker/utils/GeaneDummyUtils.hh"
#include "gm2util/tracking/MCTrackUtils.hh"

//Geometry
#include "gm2geom/coordSystems/CoordSystemsStoreData.hh"  // Coordinate transform for Residual calc.
#include "gm2geom/strawtracker/StrawTrackerGeometry_service.hh"  // Residual calc. 
#include "gm2util/coordSystems/CoordSystemUtils.hh" // Coordinate transform for Residual calc. 


//C++ includes
#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <set>
#include <math.h> 

#include <Eigen/Dense>
#include "gm2tracker/utils/GeaneEigenStorageUtils.hh"
#include "gm2tracker/utils/TrackDetailArtRecordUtils.hh"

namespace gm2strawtracker {

  //
  // Class declaration
  //
  class LowDCAsTruthLR : public art::EDAnalyzer {

  public:

    explicit LowDCAsTruthLR(fhicl::ParameterSet const& pset);

    //Override desired art::EDAnalyzer functions
    void analyze(const art::Event& event ) override;
    void beginJob() override;
    void beginRun(art::Run const & r) override;
    void endRun(art::Run const & r) override;
    

  private:

    std::string name_;

    //Producer labels

    std::string DummyModuleLabel_;
    std::string DummyInstanceName_;

    std::string DigitModuleLabel_;
    std::string DigitInstanceName_;

    std::string TrackModuleLabel_;
    std::string TrackInstanceName_;

    std::string dcaDigitModuleLabel_;
    std::string dcaDigitInstanceLabel_;

    //ROOT plotting members
    std::unique_ptr<RootManager> rootManager_;
    std::string dirName_;

    std::vector< std::string > planeFolderNames_;

    //Helper tools
    gm2geom::CoordSystemsStoreData cs_;

    gm2strawtracker::GeaneTrackUtils geaneTrackUtils_;

    double pValueCut_;
    double chi2Cut_;
    int numPlanesHitCut_;
    
    vector<double> timeWindow_;
    vector<double> momWindow_;

    // Keep track of number of tracks and number of events to work out tracks per event for this run
    int tracksInRun_;
    int eventsInRun_;
    int tracksWithWrongLRChoices_;
    int wrongLRChoices_;
    int rightLRChoices_;
    // DCA cut
    double DCACut_;

        // For setting max/min values of plots (larger for wire fit)
    std::string fitMode_;

    gm2strawtracker::GeaneDummyUtils dummyUtils_;

  }; //End of class Plotter


  //
  // Class implementation
  //

  LowDCAsTruthLR::LowDCAsTruthLR(fhicl::ParameterSet const& pset)
  : art::EDAnalyzer(pset)
  , name_( "LowDCAsSimPlots" )
  , DummyModuleLabel_( pset.get<std::string>("DummyModuleLabel",dataModuleDefs::strawBuilderModuleLabel()) )
  , DummyInstanceName_( pset.get<std::string>("DummyInstanceName","trackerdummyplane") )
  , DigitModuleLabel_( pset.get<std::string>("DigitModuleLabel",dataModuleDefs::digitModuleLabel()) )
  , DigitInstanceName_( pset.get<std::string>("DigitInstanceName",dataModuleDefs::digitInstanceLabel()) )
  , TrackModuleLabel_( pset.get<std::string>("TrackModuleLabel", dataModuleDefs::trackModuleLabel()) )
  , TrackInstanceName_( pset.get<std::string>("TrackInstanceName", dataModuleDefs::recoInstanceLabel()) )
/*  , TrackModuleLabel_( pset.get<std::string>("TrackModuleLabel") )
  , TrackInstanceName_( pset.get<std::string>("TrackInstanceName") )*/
  , dcaDigitModuleLabel_( pset.get<std::string>("dcaDigitModuleLabel",dataModuleDefs::dcaDigitModuleLabel()) )
  , dcaDigitInstanceLabel_( pset.get<std::string>("dcaDigitInstanceLabel",dataModuleDefs::digitInstanceLabel()) )
  , rootManager_()
  , dirName_( pset.get<std::string>("dirName","FinalIteration") )
  , cs_()
  , geaneTrackUtils_()
  , pValueCut_( pset.get<double>("pValueCut", 0.0) )
  , chi2Cut_( pset.get<double>("chi2Cut", 0.0) )
  , numPlanesHitCut_( pset.get<int>("numPlanesHitCut", 0))
  , timeWindow_(pset.get<vector<double> >("timeWindow",{}))
  , momWindow_(pset.get<vector<double> >("momWindow",{}))
  , tracksInRun_(0)
  , eventsInRun_(0)
  , tracksWithWrongLRChoices_(0)
  , wrongLRChoices_(0)
  , rightLRChoices_(0)
  , DCACut_( pset.get<double>("DCACut", 2500.0) ) // Set default to straw radius in mm
  , fitMode_(pset.get<string>("fitMode","badFitMode"))
  , dummyUtils_(pset)
  {}



  void LowDCAsTruthLR::beginJob() {

    // Set scale for some plots
    double boundUV = (fitMode_ == "wireFit") ? 2.535 : 1.5;

    //Create a ROOT file and manager 
    art::ServiceHandle<art::TFileService> tfs;
    auto& outputRootFile = tfs->file();
    rootManager_.reset( new RootManager(name_, &outputRootFile) ); 

    //Create directories
    auto dir = rootManager_->GetDir(&outputRootFile,dirName_,true); //true -> create if doesn't exist

    rootManager_->Add( dir, new TH1F( "Run", ";Run Number; Tracks", 1000, 1000.5, 2000.5) );

    TGraph* tgTracks = new TGraph();
    tgTracks->SetName( "TracksPerEvent" );
    tgTracks->SetTitle(";Run Number;No. Tracks per Fill");
    tgTracks->SetMarkerStyle(20);
    tgTracks->SetLineWidth(0);
    
    rootManager_->Add( dir, tgTracks);

    rootManager_->Add( dir, new TH1F( "ChiSqr", "; #chi^{2}; Tracks", 200, 0, 100) );
    rootManager_->Add( dir, new TH1F( "ChiSqrDof", "; #chi^{2}/ndf; Tracks", 100, 0, 5) );
    rootManager_->Add( dir, new TH1F( "pValues", "; pValue; Tracks", 200, 0, 1) );
    rootManager_->Add( dir, new TH1F( "Meas", "; pValue; Tracks", 200, 0, 1) );

    rootManager_->Add( dir, new TH1F( "P", "; P [MeV]; Tracks", 110, 0, 3300) );
    rootManager_->Add( dir, new TH1F( "Pu", "; P_{U} [MeV]; Tracks", 100, -800, 800) );
    rootManager_->Add( dir, new TH1F( "Pv", "; P_{V} [MeV]; Tracks", 100, -800, 800) );
    rootManager_->Add( dir, new TH1F( "U", "; U [mm]; Tracks", 100, 6500, 7000) );
    rootManager_->Add( dir, new TH1F( "V", "; V [mm]; Tracks", 100, 6500, 7000) );
    rootManager_->Add( dir, new TH1F( "Px", "; P_{x} [MeV]; Tracks", 110, 0, 3300) );
    rootManager_->Add( dir, new TH1F( "Py", "; P_{y} [MeV]; Tracks", 200, -200, 200) );
    rootManager_->Add( dir, new TH1F( "Pz", "; P_{z} [MeV]; Tracks", 200, -800, 800) );
    rootManager_->Add( dir, new TH1F( "X", "; X [mm]; Tracks", 100, -2000, 0) );
    rootManager_->Add( dir, new TH1F( "Y", "; Y [mm]; Tracks", 100, -100, 100) );
    rootManager_->Add( dir, new TH1F( "Z", "; Z [mm]; Tracks", 100, -7000, -6500) );

    // Supposed to be the overall reddisual
    rootManager_->Add( dir, new TH1F( "UVresidualsMeasPred", "; UV residual p-m (mm); Events", 100, -boundUV, boundUV) );

    rootManager_->Add( dir, new TH1F("DriftTime", ";Reco drift time [ns]", 400, -100, 150.) );
    rootManager_->Add( dir, new TH1F("DCA", ";Reco DCA [#mum]", 400, -1.e3, 3.5e3) );
    rootManager_->Add( dir, new TH1F("DCAError", ";Reco DCA Error [#mum]", 400, 0, 400) );
    //rootManager_->Add(dir, new TH1F("Width", ";Straw digit width [ns]", 96, -10., 110.) );

  }//beginJob


  void LowDCAsTruthLR::beginRun(art::Run const & r) {

    //Get coord systems
    cs_ = artg4::dataFromRunOrService<gm2geom::CoordSystemsStoreData, gm2geom::CoordSystemsStore>
    ( r, dataModuleDefs::coordSysModuleLabel(),dataModuleDefs::coordSysInstanceLabel() );
    if( cs_.size() == 0 ) {
      throw cet::exception(name_) << "This run does not contain any data associated with the coordinate system\n";
      
    }

    // Pass coord system to GeaneDummyUtils (to know LR)
    dummyUtils_.fillCS(cs_);

    // Reset tracks and events
    eventsInRun_ = 0;
    tracksInRun_ = 0;

  }//beginRun


  void LowDCAsTruthLR::analyze(const art::Event& event) {

    if(event.isRealData()){
      throw cet::exception(name_) << "You cannot run this module on real data, it is for truth LR comparison)\n";
    }

    // Get StrawDigitArtRecordCollection
    art::Handle<gm2strawtracker::StrawDigitArtRecordCollection> DigitDataHandle;
    bool foundDigitcollection = event.getByLabel(DigitModuleLabel_,DigitInstanceName_,DigitDataHandle);
    if( !foundDigitcollection ){
      throw cet::exception(name_) << "No StrawDigitArtRecordCollection in this event (\"" << DigitModuleLabel_ << "\":\"" << DigitInstanceName_ << "\")\n";
    }

  // Get TrackDetailArtRecordCollection
    art::Handle<gm2strawtracker::TrackDetailArtRecordCollection> TrackDetailDataHandle;
    bool foundTrackcollection = event.getByLabel(TrackModuleLabel_,TrackInstanceName_,TrackDetailDataHandle);
    if( !foundTrackcollection ) {
      throw cet::exception("Plotter") << "No Trackcollection in this event (\"" << TrackModuleLabel_ << "\":\"" << TrackInstanceName_ << "\")\n";
      return;
    } 

    // Get GhostDetectorArtRecordCollection
    art::Handle<gm2truth::GhostDetectorArtRecordCollection> DummyDataHandle;
    bool foundDummycollection = event.getByLabel(DummyModuleLabel_,DummyInstanceName_,DummyDataHandle);
    if( ! foundDummycollection ) {
      throw cet::exception("Plotter") << "No Dummycollection in this event (\"" << DummyModuleLabel_ << "\":\"" << DummyInstanceName_ << "\")\n";
      return;
    } 

    // Vectors of ArtRecords
    gm2strawtracker::StrawDigitArtRecordCollection digits = *DigitDataHandle;
    gm2strawtracker::TrackDetailArtRecordCollection tracks = *TrackDetailDataHandle;
    gm2truth::GhostDetectorArtRecordCollection dummys = *DummyDataHandle;

    // Loop over tracks
    for( auto track : *TrackDetailDataHandle ) {

      // Skip failed tracks - dummyPlaneHits is only filled for non-failed ones
      if(track.failureMode != 0) continue;
      
      // THINK ABOUT WHAT OTHER CUTS YOU WANT HERE - DO YOU WANT ANY?
      // YOU MIGHT WANT TO MAKE PLOTS THAT TELL YOU WHAT THE EFFECT OF EACH CUT IS ON THE NUMBER OF WRONG L/R CHOICES

      // Fill stationStr as this is used in fillLRFromTruth for coord-system transform
      int stationNum = track.candidate->strawDigits.at(0)->wireID.getStation();
      dummyUtils_.fillStationStr(Form("TrackerStation[%d]",stationNum),stationNum);

      // Fill with truth LR hit sides
      dummyUtils_.fillLRFromTruth(track);

      // Store true hit sides
      std::string trueHitStr = "";
      for(auto& trueHitSide : dummyUtils_.trueHitSides){
	if(trueHitSide == gNA_side)      trueHitStr += "-";
	else if(trueHitSide == gLeft)    trueHitStr += "L";
	else if(trueHitSide == gRight)   trueHitStr += "R";
	else if(trueHitSide == gCenter)  trueHitStr += "C";
	else if(trueHitSide == gUnknown) trueHitStr += "U";
      }

      // Store reconstructed hit sides
      std::string recoHitStr = "";
      for(auto& recoHitSide : track.geaneHits.geaneHitSides){
	if(recoHitSide == gNA_side)      recoHitStr += "-";
	else if(recoHitSide == gLeft)    recoHitStr += "L";
	else if(recoHitSide == gRight)   recoHitStr += "R";
	else if(recoHitSide == gCenter)  recoHitStr += "C";
	else if(recoHitSide == gUnknown) recoHitStr += "U";
      }

      // Look for wrong L/R choices.
      // Try to catch cases such as when reco side is "C" but true hit side will still be "L" or "R".
      // May be other cases I've not thought about here
      bool wrongHitFound = false;
      std::string wrongHitStr = "";
      for (unsigned int i = 0; i < track.geaneHits.geaneHitSides.size(); ++i){
	if(dummyUtils_.trueHitSides.at(i) == track.geaneHits.geaneHitSides.at(i)) wrongHitStr += "-";
	else if(track.geaneHits.geaneHitSides.at(i) == gCenter)                   wrongHitStr += "?";
	else {

	  // This L/R choice was wrong - record here, but we also want to add plots of DCA and anything else we want to study...
	  wrongHitStr += "X";
	  wrongLRChoices_++;

	  // Record that this track had at least one L/R wrong
	  if(!wrongHitFound){
	    tracksWithWrongLRChoices_++;
	    wrongHitFound = true;
	  }
	}

	// You'll want a plot of all DCAs here so you can normalise your wrong L/R choices one to make a plot of fraction of incorrect L/R vs DCA

      }

      std::cout << "=================================================" << std::endl;
      std::cout << "TRUE HIT SIDES:  " << trueHitStr << std::endl;
      std::cout << "RECO HIT SIDES:  " << recoHitStr << std::endl;
      std::cout << "WRONG HIT SIDES: " << wrongHitStr << std::endl;


      // Record track level data here.
      // For example if you want to look at p-value vs fraction of tracks with wrong L/R:
      // hPvalueAll->Fill(track.pValue);
      // if(wrongHitFound) hPValueWrongLR->Fill(track.pValue);
      // Then take ratio of these bin-by-bin in endRun (or in macro if you're going to parallelise) to get fraction of tracks with wrong L/R vs p-value

      tracksInRun_++;

    }

    eventsInRun_++;    

  }


  void LowDCAsTruthLR::endRun(art::Run const & r) {

    auto tgTracks = rootManager_->Get<TGraph*>(rootManager_->GetDir(dirName_), "TracksPerEvent" );
    if(eventsInRun_ > 0) tgTracks->SetPoint(tgTracks->GetN(), r.run(), tracksInRun_/eventsInRun_);

    if(timeWindow_.size()==0) std::cout << "*** Run = " << r.run() << "\tEvents = " << eventsInRun_ << "\tTracks = " << tracksInRun_ << "\ttracksWithWrongLRChoices = " << tracksWithWrongLRChoices_ << "\twrongLRChoices = " << wrongLRChoices_ << std::endl;

  }

} // End of namespace gm2strawtracker


// These are some necessary boilerplate for the ROOT persistency system
using gm2strawtracker::LowDCAsTruthLR;
DEFINE_ART_MODULE(LowDCAsTruthLR)
