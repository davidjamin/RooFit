import sys
import ROOT as r
infile = r.TFile.Open('/afs/cern.ch/user/d/djamin/fcc_work/FlatTreeAnalyzer/outputs/analysis_fcc_v02/good/tth_boosted/alljets/root_ttH/histos.root')

def Sign(x):
 return abs(x) == x

low_x=50
high_x=300

#######ttj
h_ttj_SR=infile.Get('tt+jets_sel3_h_mjj_l2') # >=4 btag
h_ttj_CR=infile.Get('tt+jets_sel4_h_mjj_l2') # <4 btag CR
h_ttj_CR.Scale(h_ttj_SR.Integral()/h_ttj_CR.Integral())
h_ttj=h_ttj_CR
h_ttj.Smooth()

#######ttbb
h_ttbb=infile.Get('tt+bb_sel3_h_mjj_l2')
h_ttbb.Smooth()

## fits
h_ttbkg=h_ttj.Clone()
h_ttbkg.Add(h_ttbb)
myfit = r.TF1("myfit","pol5", low_x, high_x)
h_ttbkg.Fit("myfit","S","",low_x, high_x)
#h_ttbkg.Fit("myfit")

parl1_0 = 600.
parl1_1 = 20.
parl2_0 = 600.
parl2_1 = -3.

my_line1 = r.TF1("my_line1","pol1", low_x, high_x)
my_line1.SetParameters(parl1_0,parl1_1)

my_line2 = r.TF1("my_line2","pol1", low_x, high_x)
my_line2.SetParameters(parl2_0,parl2_1)

## hist from fits
h_ttbkg_fit=h_ttj.Clone()
h_ttbkg_fitup=h_ttj.Clone()
h_ttbkg_fitdo=h_ttj.Clone()
for i_bin in xrange( 1, h_ttbkg_fit.GetNbinsX()+1 ):
  bin_val = myfit.Eval(h_ttbkg_fit.GetBinCenter(i_bin))
  h_ttbkg_fit.SetBinContent(i_bin, bin_val)
  #
  the_val = my_line1.Eval(h_ttbkg_fit.GetBinCenter(i_bin))
  if the_val<0. : the_val=0.
  bin_valerrup = bin_val * the_val
  h_ttbkg_fitup.SetBinContent(i_bin, bin_valerrup)
  #
  the_val = my_line2.Eval(h_ttbkg_fit.GetBinCenter(i_bin))
  if the_val<0. : the_val=0.
  bin_valerrdo = bin_val * the_val
  h_ttbkg_fitdo.SetBinContent(i_bin, bin_valerrdo)

Ninit=h_ttbkg_fit.Integral(low_x, high_x)
h_ttbkg_fit.SetLineWidth(3)
h_ttbkg_fit.SetLineColor(r.kGreen+3)
h_ttbkg.SetLineColor(r.kBlack)
#
Nfitup=h_ttbkg_fitup.Integral(low_x, high_x)
h_ttbkg_fitup.Scale(Ninit/Nfitup)
h_ttbkg_fitup.SetLineWidth(3)
h_ttbkg_fitup.SetLineColor(r.kRed)
#
Nfitdo=h_ttbkg_fitdo.Integral(low_x, high_x)
h_ttbkg_fitdo.Scale(Ninit/Nfitdo)
h_ttbkg_fitdo.SetLineWidth(3)
h_ttbkg_fitdo.SetLineColor(r.kBlue)

r.gStyle.SetOptStat(0)

h_ttbkg_fitdo.GetXaxis().SetRangeUser(low_x, high_x)
h_ttbkg_fitdo.SetTitle("")
c = r.TCanvas("plot", "plot", 800, 800)
h_ttbkg_fitdo.Draw()
h_ttbkg_fitup.Draw("same")
h_ttbkg.Draw("same")
h_ttbkg_fit.Draw("same")
c.SaveAs("check_fit.eps")

## ratio
h_ratio_up=h_ttbkg_fitup.Clone()
h_ratio_up.Add(h_ttbkg_fit,-1.)
h_ratio_up.Divide(h_ttbkg_fit)
#
h_ratio_do=h_ttbkg_fitdo.Clone()
h_ratio_do.Add(h_ttbkg_fit,-1.)
h_ratio_do.Divide(h_ttbkg_fit)

h_ratio_up.GetXaxis().SetRangeUser(low_x, high_x)
maxi=max(h_ratio_up.GetMaximum(),h_ratio_do.GetMaximum())
mini=min(h_ratio_up.GetMinimum(),h_ratio_do.GetMinimum())
h_ratio_up.SetMinimum(mini)
h_ratio_up.SetMaximum(maxi)
h_ratio_up.SetTitle("")
c2 = r.TCanvas("plot1", "plot1", 800, 800)
h_ratio_up.Draw()
h_ratio_do.Draw("same")
c2.SaveAs("check_fit_ratio.eps")

#print "h="+str(h_ttbkg_fit.Integral(low_x, high_x))
#print "hdo="+str(h_ttbkg_fitdo.Integral(low_x, high_x))
#print "hup="+str(h_ttbkg_fitup.Integral(low_x, high_x))

