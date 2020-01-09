# Plotter for truth LR information
# !!! - Fraction of tracks with wrong LR guess !!!
# - Fraction of tracks with p-values below 5%
# - Reduced chi^2


from ROOT import TFile, TCanvas, TH1F, TH1D, TLegend, TAxis, TAttMarker, TGraph, TGraphErrors
from ROOT import gROOT
from array import array

# # Return the number of tracks with a p-value less than 5%
# def pValFrac(hist):

# 	# Loop over the bins
# 	# Get bin values
# 	# Sum them
# 	# Break when x-value is 5%
# 	# Divide by total entries

# 	binVal = 0
# 	for bin in range(0, hist.GetNbinsX()):
# 		xVal = hist.GetBinCenter(bin+1)
# 		# print(xVal)
# 		# binVal = hist.GetBinContent(bin+1) + binVal
# 		if(xVal < 0.05):
# 			binVal = hist.GetBinContent(bin+1) + binVal
# 			frac = binVal / hist.GetEntries()

# 			return frac

# 			def wrongHitsFrac(allHist, wrongHist):

# 				return  wrongHist.GetEntries() / allHist.GetEntries()

def Frac(all_, rightOrWrong_):

	frac = []

	for i in range(0,len(all_)):

		frac.append(rightOrWrong_[i].GetEntries() / all_[i].GetEntries())

		print(str(rightOrWrong_[i].GetEntries())+" * "+str(all_[i].GetEntries()))

	return frac

def DrawScat(y_, DCAs_, title, fname):

	c = TCanvas("c2","",800,600)

	# Normal arrays don't work for whatever reason, must be a ROOT thing
	x, y, ex, ey = array('d'), array('d'), array('d'), array('d')

	n = len(y_)

	# if(n != len(wrongHist)):
		# print("*** Error, hist arrays different length ***")
		# return

	for i in range(0,n):

#		frac = wrong_[i].GetEntries() / all_[i].GetEntries()
		x.append(DCAs_[i])
		ex.append(0)
		y.append(y_[i])
		ey.append(0)

		# print(str(DCAs_[i])+" * "+str(y_)+" * "+str(wrong_[i].GetEntries())+" * "+str(all_[i].GetEntries()))

	scat = TGraphErrors(n,x,y,ex,ey)
	scat.SetTitle(title)
			
	scat.GetXaxis().SetTitleSize(.04)
	scat.GetYaxis().SetTitleSize(.04)
	scat.GetXaxis().SetTitleOffset(1.1)
	scat.GetYaxis().SetTitleOffset(1.25)
	scat.GetXaxis().CenterTitle(1)
	scat.GetYaxis().CenterTitle(1)
	# scat.GetYaxis().SetRangeUser(0.086,0.106)
	scat.GetXaxis().SetRangeUser(-5,2500)
	scat.GetYaxis().SetMaxDigits(4)
	#scat.SetMarkerSize(3)
	#scat.SetLineWidth(3)
	scat.SetMarkerStyle(20) # Full circle
	#scat.SetMarkerColor(4)
	#scat.SetLineColor(4)
	scat.Draw("AP")
	c.SaveAs(fname)

	return


file = TFile.Open("~/Documents/gm2/LowDCAs/plots/LowDCAs_SimScanLongPlotsFull.root")

# Real dumb bit of logic here
#DCAsArray_ = [0,25,50,75,100,125,150,175,200,225,250,275,300,325,350,375,400,425,450,475,500]
#DCAsArray_ = [0,100,200,300,400,500,600,125,150,175,200,225,250,275,300,325,350,375,400,425,450,475,500]
DCAsArray_ = list(range(0,2400,100))
# 
# histType = ["Run","pValues"]
# nameType = ["Fraction of wrong tracks","Fraction of tracks with p-value < 5%"]

# Loop over histogram types



allHits_ = []
wrongHits_ = []
rightHits_ = []
# fracHits = []

# Loop over DCA scan
for ihist in range(0,len(DCAsArray_)):
	print("Tracks",ihist)

	allHits_.append(file.Get("plots"+str(ihist)+"/AllHits/Run"))
	wrongHits_.append(file.Get("plots"+str(ihist)+"/WrongHits/Run"))
	rightHits_.append(file.Get("plots"+str(ihist)+"/RightHits/Run"))	

		# print(DCAsArray[ihist],pValFrac(allHits[ihist]))

	# print("len(allHits) "+str(len(allHits)))
	# print("allHits[0].GetMean() "+str(allHits[0].GetMean()))


	#typeFlag = 0
	#if (itype > 1): typeFlag = 1

	#mean = "Mean "
	#if (typeFlag == 1): mean = "" 

	
	#print("Threshold [um] * "+histType[itype])
	# DrawScat(histsArrayData, DCAsArray, typeFlag, ";Low DCA threshold [#mum];"+mean+nameType[itype],"../Plots-25-11-19/"+histType[itype]+"Scat500_DATA.pdf")

DrawScat(Frac(allHits_, wrongHits_), DCAsArray_, ";Low DCA threshold [#mum];Fraction of tracks with wrong LR", "Plots/FracWrongTracksLong.png")
DrawScat(Frac(allHits_, rightHits_), DCAsArray_, ";Low DCA threshold [#mum];Fraction of tracks with right LR", "Plots/FracRightTracksLong.png")


# draw1D(histsArrayCut, DCAsArray, ";p-value;Tracks / 0.005","../Plots/pValues1DExtreme.pdf")
# drawScat(histsArrayCut, DCAsArray, ";Low DCA Threshold [#mum];Mean p-value","../Plots/pValuesScatExtreme.pdf")