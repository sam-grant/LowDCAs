# Plotter for truth LR information
# !!! - Fraction of tracks with wrong LR guess !!!
# - Fraction of tracks with p-values below 5%
# - Reduced chi^2


#
# ONLY USE THIS PLOTTER FOR TRUTH STUFF! 
#


from ROOT import TFile, TCanvas, TH1F, TH1D, TLegend, TAxis, TAttMarker, TGraph, TGraphErrors
from ROOT import gROOT
from array import array

def Ratio(wrongHist, allHist, rebin):

	# Clone to be safe
	allHist.Rebin(rebin)
	wrongHist.Rebin(rebin)

	ratio = wrongHist.Clone("ratio")

	ratio.Divide(allHist)

	return ratio


def Mean(all_):

	means_ = []

	for ihist in range(len(all_)):

		means_.append(all_[ihist].GetMean())

	return means_

# Return the number of tracks with a p-value less than 5%

def pValFrac(all_):

 	# Loop over the bins
 	# Get bin x-values
 	# if x-value is < 5%, sum the bin contents
 	# Divide by total entries
 	tracksLessThan_ = []

 	for ihist in range(0,len(all_)):

 		tracks = 0

 		for bin in range(0, all_[ihist].GetNbinsX()):

 			pValue = all_[ihist].GetBinCenter(bin+1)
 			# print("p-value", pValue)
 			# binVal = hist.GetBinContent(bin+1) + binVal
 			if(pValue < 0.05):

 				tracks = all_[ihist].GetBinContent(bin+1) + tracks
 				# fraction = binVal / hist.GetEntries()

 		# print("tracks ",tracks)

 		tracksLessThan_.append(tracks / all_[ihist].GetEntries())

 	return tracksLessThan_

def TotalTracks(all_):
	totalTracks_ = []
	for i in range(len(all_)):
		totalTracks_.append(all_[i].GetEntries())
	return totalTracks_

def Frac(rightOrWrong_, all_):
	frac_ = []
	for i in range(0,len(all_)):
		# print("rightOrWrong_[i].GetEntries() ",rightOrWrong_[i].GetEntries())
		# print("all_[i].GetEntries() ",all_[i].GetEntries())
		frac_.append(rightOrWrong_[i].GetEntries() / all_[i].GetEntries() )
	return frac_

def DrawHist1D(hist,title,fname,i): 

	c1 = TCanvas("c1","",800,600)

	# hist.Rebin(4)
	hist.SetStats(0)

	hist.SetTitle(title)
			
	hist.GetXaxis().SetTitleSize(.04)
	hist.GetYaxis().SetTitleSize(.04)
	hist.GetXaxis().SetTitleOffset(1.1)
	hist.GetYaxis().SetTitleOffset(1.25)
	hist.GetXaxis().CenterTitle(1)
	hist.GetYaxis().CenterTitle(1)
	# hist.GetYaxis().SetRangeUser(.5,.7)
	if(i==0): hist.GetXaxis().SetRangeUser(-5,505)
	if(i==1): hist.GetXaxis().SetRangeUser(-5,2505)

	# hist.GetYaxis().SetRangeUser(0.50,0.70)
	hist.GetYaxis().SetMaxDigits(4)

	hist.SetLineWidth(3)
	hist.SetLineColor(1)

	hist.Draw()
	c1.SaveAs(fname)

def DefineScat(y_, x_):

	x, y, ex, ey = array('d'), array('d'), array('d'), array('d')

	n = len(y_)

	for i in range(0,n):

#		frac = wrong_[i].GetEntries() / all_[i].GetEntries()
		x.append(x_[i])
		ex.append(0)
		y.append(y_[i])
		ey.append(0)

		# print(str(DCAs_[i])+" * "+str(y_)+" * "+str(wrong_[i].GetEntries())+" * "+str(all_[i].GetEntries()))

	return TGraphErrors(n,x,y,ex,ey)


def DrawScat(plot, title, fname):

	c2 = TCanvas("c2","",800,600)

	plot.SetTitle(title)			
	plot.GetXaxis().SetTitleSize(.04)
	plot.GetYaxis().SetTitleSize(.04)
	plot.GetXaxis().SetTitleOffset(1.1)
	plot.GetYaxis().SetTitleOffset(1.25)
	plot.GetXaxis().CenterTitle(1)
	plot.GetYaxis().CenterTitle(1)
	# plot.GetYaxis().SetRangeUser(0.086,0.106)\
	# plot.GetYaxis().SetRangeUser(0.5,0.7)
	# plot.GetXaxis().SetRangeUser(-5,2500)
	plot.GetYaxis().SetMaxDigits(4)
	#plot.SetMarkerSize(3)
	#plot.SetLineWidth(3)
	plot.SetMarkerStyle(20) # Full circle
	#plot.SetMarkerColor(4)
	#plot.SetLineColor(4)
	plot.Draw("AP")
	c2.SaveAs(fname)

	return

def DrawScatOverlay(plot1, plot2, title, fname):

	c2 = TCanvas("c2","",800,600)

	leg = TLegend(0.11,0.69,0.69,0.89)
	leg.SetBorderSize(0)

	plot1.SetTitle(title)			
	plot1.GetXaxis().SetTitleSize(.04)
	plot1.GetYaxis().SetTitleSize(.04)
	plot1.GetXaxis().SetTitleOffset(1.1)
	plot1.GetYaxis().SetTitleOffset(1.25)
	plot1.GetXaxis().CenterTitle(1)
	plot1.GetYaxis().CenterTitle(1)
	# plot.GetYaxis().SetRangeUser(0.086,0.106)
	# plot1.GetXaxis().SetRangeUser(-5,505)
	plot1.GetYaxis().SetMaxDigits(4)
	plot1.GetYaxis().SetRangeUser(0,1)
	#plot.SetMarkerSize(3)
	#plot.SetLineWidth(3)
	plot1.SetMarkerStyle(20) # Full circle
	plot2.SetMarkerStyle(24) # Open circle
	#plot.SetMarkerColor(4)
	#plot.SetLineColor(4)

	leg.AddEntry(plot1, "Fraction of tracks with a wrong LR choice")
	leg.AddEntry(plot2, "Fraction of tracks with an ambiguous LR choice")
	
	plot1.Draw("AP")
	plot2.Draw("P same")

	leg.Draw("same")

	c2.SaveAs(fname)

	return

# Wrap main in a function
def main():

	shortFile = TFile.Open("~/Documents/gm2/LowDCAs/ROOT/LowDCAsPlots500_main.root")
	#shortFile = TFile.Open("~/Documents/gm2/LowDCAs/ROOT/LowDCAs_SimScanPlotsFull_Ambiguous.root")
	longFile = TFile.Open("~/Documents/gm2/LowDCAs/ROOT/LowDCAsPlotsExtreme-25-11-19.root")
	
	# DCA threshold arrays, short and long
	DCAs_ = [list(range(0,525,25)), list(range(0,2600,100))]
	# 
	# histType = ["Run","pValues"]
	# nameType = ["Fraction of wrong tracks","Fraction of tracks with p-value < 5%"]
	
	# Loop over histogram types

	files_ = [shortFile, longFile]

	#fileType = ".png"
	fileType = ".pdf"

	#
	# Take ratio of all and wrong DCAs
	# 


	# ratio_ = []

	# for i_ratio in range(0,2):

	# 	ratio = Ratio(files_[i_ratio].Get("plots0/WrongHits/DCA"), files_[i_ratio].Get("plots0/AllHits/DCA"), 1)
	# 	#ratio = Ratio(files_[0].Get("plots0/WrongHits/DCA"), files_[0].Get("plots0/AllHits/DCA"), 1)
	DrawHist1D(files_[0].Get("plots0/DCA"), ";Measured DCA [#mum];Hits", "../TestPlots/DCAsRecoShort"+str(0)+fileType, 0)
	DrawHist1D(files_[1].Get("plots0/DCA"), ";Measured DCA [#mum];Hits", "../TestPlots/DCAsRecoLong"+str(0)+fileType, 1)
	# 	DrawHist1D(ratio, ";Measured DCA [#mum];Fraction of hits with a wrong LR choice", "../HitLevelPlots/DCARatio"+str(i_ratio)+fileType, i_ratio)
	# DrawHist1D(ratio, ";Measured DCA [#mum];Fraction of tracks with a wrong LR choice", "../TrackLevelPlots/DCARatio"+fileType)

	# fracHits = []
	
	# Loop over DCA scan
	for ifile in range(0,2):
	
		print("ifile",ifile)
	
		allHitsTracks_ = []
		allHitsPValues_ = []
		allHitsChiSqrDof_ = []

		# wrongHitsTracks_ = []
		# wrongHitsPValues_ = []
		# wrongHitsChiSqrDof_ = []

		# rightHitsTracks_ = []
		# rightHitsPValues_ = []
		# rightHitsChiSqrDof_ = []

		# ambiguousHitsTracks_ = []
		# ambiguousHitsPValues_ = []
		# ambiguousHitsChiSqrDof_ = []
		
		for ihist in range(0,len(DCAs_[ifile])):
	
			# print(files_[ifile])
			# print(DCAs_[ifile])
	
			allHitsTracks_.append(files_[ifile].Get("plots"+str(ihist)+"/Run"))
			allHitsPValues_.append(files_[ifile].Get("plots"+str(ihist)+"/pValues"))
			allHitsChiSqrDof_.append(files_[ifile].Get("plots"+str(ihist)+"/ChiSqrDof"))

			# wrongHitsTracks_.append(files_[ifile].Get("plots"+str(ihist)+"/WrongHits/Run"))
			# wrongHitsPValues_.append(files_[ifile].Get("plots"+str(ihist)+"/WrongHits/pValues"))
			# wrongHitsPValues_.append(files_[ifile].Get("plots"+str(ihist)+"/WrongHits/ChiSqrDof"))

			# rightHitsTracks_.append(files_[ifile].Get("plots"+str(ihist)+"/RightHits/Run"))	
			# rightHitsPValues_.append(files_[ifile].Get("plots"+str(ihist)+"/RightHits/pValues"))
			# rightHitsChiSqrDof_.append(files_[ifile].Get("plots"+str(ihist)+"/RightHits/ChiSqrDof"))

			# ambiguousHitsTracks_.append(files_[ifile].Get("plots"+str(ihist)+"/AmbiguousHits/Run"))	
			# ambiguousHitsPValues_.append(files_[ifile].Get("plots"+str(ihist)+"/AmbiguousHits/pValues"))
			# ambiguousHitsChiSqrDof_.append(files_[ifile].Get("plots"+str(ihist)+"/AmbiguousHits/ChiSqrDof"))

		# print(DCAsArray[ihist],pValFrac(allHits[ihist]))
	
		# print("len(allHits) "+str(len(allHits)))
		# print("allHits[0].GetMean() "+str(allHits[0].GetMean()))
	
	
		#typeFlag = 0
		#if (itype > 1): typeFlag = 1
	
		#mean = "Mean "
		#if (typeFlag == 1): mean = "" 

		
		#print("Threshold [um] * "+histType[itype])
		# DrawScat(histsArrayData, DCAsArray, typeFlag, ";Low DCA threshold [#mum];"+mean+nameType[itype],"../Plots-25-11-19/"+histType[itype]+"Scat500_DATA.pdf")
		if(ifile == 0):

			# All tracks
			DrawScat(DefineScat(TotalTracks(allHitsTracks_), DCAs_[ifile]), ";Low DCA threshold [#mum];Total number of tracks", "../TestPlots/TotalTrackRecoShort"+fileType)
			DrawScat(DefineScat(pValFrac(allHitsPValues_), DCAs_[ifile]), ";Low DCA threshold [#mum];Fraction of tracks with p-value < 5%", "../TestPlots/pValueRecoFracShort"+fileType)
			# DrawScat(DefineScat(pValFrac(wrongHitsPValues_), DCAs_[ifile]), ";Low DCA threshold [#mum];Fraction of wrong LR tracks with p-value < 5%", "../TestPlots/pValueWrongFracShort"+fileType)
			# DrawScat(DefineScat(pValFrac(ambiguousHitsPValues_), DCAs_[ifile]), ";Low DCA threshold [#mum];Fraction of ambiguous LR tracks with p-value < 5%", "../TestPlots/pValueAmbiguousFracShort"+fileType)
			DrawScat(DefineScat(Mean(allHitsPValues_), DCAs_[ifile]), ";Low DCA threshold [#mum];Mean p-value", "../TestPlots/pValueMeansRecoShort"+fileType)
			# Fractions of each type of track
			# DrawScat(DefineScat(Frac(wrongHitsTracks_, allHitsTracks_), DCAs_[ifile]), ";Low DCA threshold [#mum];Fraction of tracks with a wrong LR choice", "../TestPlots/FracWrongTracksShort"+fileType)
			# DrawScat(DefineScat(Frac(rightHitsTracks_, allHitsTracks_), DCAs_[ifile]), ";Low DCA threshold [#mum];Fraction of tracks with only correct LR choices", "../TestPlots/FracRightTracksShort"+fileType)
			# DrawScat(DefineScat(Frac(ambiguousHitsTracks_, allHitsTracks_), DCAs_[ifile]), ";Low DCA threshold [#mum];Fraction of tracks with an ambiguous LR choice", "../TestPlots/FracAmbiguousTracksShort"+fileType)

			# DrawScatOverlay(DefineScat(Frac(wrongHitsTracks_, allHitsTracks_), DCAs_[ifile]),DefineScat(Frac(ambiguousHitsTracks_, allHitsTracks_), DCAs_[ifile]),";Low DCA threshold [#mum];Fraction of tracks","../TestPlots/FracWrongAmbTracksShort"+fileType)
		
		else:

			# print("Not using long scan, sorry too complicated")
			# All tracks
			DrawScat(DefineScat(TotalTracks(allHitsTracks_), DCAs_[ifile]), ";Low DCA threshold [#mum];Total number of tracks", "../TestPlots/TotalTracksRecoLong"+fileType)
			DrawScat(DefineScat(Mean(allHitsPValues_), DCAs_[ifile]), ";Low DCA threshold [#mum];Mean p-value", "../TestPlots/pValueMeansRecoLong"+fileType)
			# DrawScat(DefineScat(Mean(allHitsChiSqrDof_), DCAs_[ifile]), ";Low DCA threshold [#mum];Mean #chi^{2}/ndf", "../TestPlots/chiSqrDofLong"+fileType)
			DrawScat(DefineScat(pValFrac(allHitsPValues_), DCAs_[ifile]), ";Low DCA threshold [#mum];Fraction of tracks with p-value < 5%", "../TestPlots/pValueFracRecoLong"+fileType)
			# # DrawScat(DefineScat(pValFrac(wrongHitsPValues_), DCAs_[ifile]), ";Low DCA threshold [#mum];Fraction of wrong LR tracks with p-value < 5%", "../TestPlots/pValueWrongFracLong"+fileType)
			# # DrawScat(DefineScat(pValFrac(ambiguousHitsPValues_), DCAs_[ifile]), ";Low DCA threshold [#mum];Fraction of ambiguous LR tracks with p-value < 5%", "../TestPlots/pValueAmbiguousFracLong"+fileType)
			# 
			# # Fractions of each type of track
			# DrawScat(DefineScat(Frac(wrongHitsTracks_, allHitsTracks_), DCAs_[ifile]), ";Low DCA threshold [#mum];Fraction of tracks with a wrong LR choice", "../TestPlots/FracWrongTracksLong"+fileType)
			# DrawScat(DefineScat(Frac(rightHitsTracks_, allHitsTracks_, ), DCAs_[ifile]), ";Low DCA threshold [#mum];Fraction of tracks with only right LR choices", "../TestPlots/FracRightTracksLong"+fileType)
			# DrawScat(DefineScat(Frac(ambiguousHitsTracks_, allHitsTracks_, ), DCAs_[ifile]), ";Low DCA threshold [#mum];Fraction of tracks with an ambiguous LR choice", "../TestPlots/FracAmbiguousTracksLong"+fileType)
	
	
	
	# draw1D(histsArrayCut, DCAsArray, ";p-value;Tracks / 0.005","../Plots/pValues1DExtreme.pdf")
	# drawScat(histsArrayCut, DCAsArray, ";Low DCA Threshold [#mum];Mean p-value","../Plots/pValuesScatExtreme.pdf")

# Execute main
if __name__ == "__main__":
	main()








