from ROOT import TFile, TCanvas, TH1F, TH1D, TLegend, TAxis, TAttMarker, TGraph, TGraphErrors
from ROOT import gROOT
from array import array


def DrawScat(hists, DCAs, flag, title, fname):

	c = TCanvas("c2","",800,600)

	# Normal arrays don't work for whatever reason, must be a ROOT thing
	x, y, ex, ey = array('d'), array('d'), array('d'), array('d')
	n = len(hists);

	for i in range(0,n):

		if (flag == 0): 
			print(str(DCAs[i])+" * "+str(hists[i].GetMean()))
			x.append(DCAs[i])
			ex.append(0)
			y.append(hists[i].GetMean())
			ey.append(hists[i].GetMeanError())
		else: 
			print(str(DCAs[i])+" * "+str(hists[i].GetEntries()))
			x.append(DCAs[i])
			ex.append(0)
			y.append(hists[i].GetEntries())
			ey.append(0)



	scat = TGraphErrors(n,x,y,ex,ey)
	scat.SetTitle(title)
	scat.GetXaxis().SetTitleSize(.04)
	scat.GetYaxis().SetTitleSize(.04)
	scat.GetXaxis().SetTitleOffset(1.1)
	scat.GetYaxis().SetTitleOffset(1.25)
	scat.GetXaxis().CenterTitle(1)
	scat.GetYaxis().CenterTitle(1)
	# scat.GetYaxis().SetRangeUser(0.086,0.106)
	scat.GetXaxis().SetRangeUser(-5,505)
	scat.GetYaxis().SetMaxDigits(4)
	#scat.SetMarkerSize(3)
	#scat.SetLineWidth(3)
	scat.SetMarkerStyle(20) # Full circle
	#scat.SetMarkerColor(4)
	#scat.SetLineColor(4)
	scat.Draw("AP")
	c.SaveAs(fname)


fData = TFile.Open("~/Documents/gm2/LowDCAs/ROOT/LowDCAsPlots500-25-11-19.root")
# fData = TFile.Open("~/Documents/gm2/LowDCAs/ROOT/LowDCAsPlots500.root")
fSim = TFile.Open("~/Documents/gm2/LowDCAs/ROOT/LowDCAsSimPlots500All-25-11-19.root")

DCAsArray = [0,25,50,75,100,125,150,175,200,
			 225,250,275,300,325,350,375,400,
			 425,450,475,500]

histType = ["pValues","ChiSqrDof","Run"]
nameType = ["p-value","#chi^{2}/ndf","Number of tracks"]

for itype in range(0,len(histType)):

	# Put histograms in an array
	histsArrayData = []
	histsArraySim = []

	for ihist in range(0,len(DCAsArray)):
		# print("Tracks",ihist)
		histsArrayData.append(fData.Get("plots"+str(ihist)+"/"+histType[itype]))
		histsArraySim.append(fSim.Get("plots"+str(ihist)+"/"+histType[itype]))
	
	typeFlag = 0
	if (itype > 1): typeFlag = 1

	mean = "Mean "
	if (typeFlag == 1): mean = "" 
	
	print("\n********** DATA **********\n")
	print("Threshold [um] * "+histType[itype])
	DrawScat(histsArrayData, DCAsArray, typeFlag, ";Low DCA threshold [#mum];"+mean+nameType[itype],"../Plots-25-11-19/"+histType[itype]+"Scat500_DATA.pdf")
	print("\n********** SIM **********\n")
	print("Threshold [um] * "+histType[itype])
	DrawScat(histsArraySim, DCAsArray, typeFlag, ";Low DCA threshold [#mum];"+mean+nameType[itype],"../Plots-25-11-19/"+histType[itype]+"Scat500_SIM.pdf")



# draw1D(histsArrayCut, DCAsArray, ";p-value;Tracks / 0.005","../Plots/pValues1DExtreme.pdf")
# drawScat(histsArrayCut, DCAsArray, ";Low DCA Threshold [#mum];Mean p-value","../Plots/pValuesScatExtreme.pdf")
