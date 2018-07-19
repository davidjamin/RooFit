import sys
import ROOT as r

mode = 0
if len(sys.argv)>1: mode = int(sys.argv[1])

#infile = r.TFile.Open('/afs/cern.ch/user/d/djamin/fcc_work/FlatTreeAnalyzer/outputs/analysis_fcc_v02/good/tth_boosted/alljets/root_ttH/histos.root')
infile = r.TFile.Open('/eos/experiment/fcc/hh/analyses/Higgs/ttH/FlatTreeAnalyzer_outputs/fcc_v02/May2018_highstat_prod/root_ttH/histos.root')
infile = r.TFile.Open('/eos/experiment/fcc/hh/analyses/Higgs/ttH/FlatTreeAnalyzer_outputs/fcc_v02/May2018_highstat_prod/good_sel_2D_optim_tail_removal/root_ttH/histos.root')

the_bin='_l150'
do_shape=True
#do_shape=False

#def Sign(x):
# return abs(x) == x

low_x=50
high_x=250

#######ttj
h_ttj_SR=infile.Get('tt+jets_sel0_h_m2j'+the_bin) # >=4 btag
h_ttj_CR=infile.Get('tt+jets_sel0_h_m2j'+the_bin) # <4 btag CR
#h_ttj_CR=infile.Get('tt+jets_sel6_h_m2j'+the_bin) # <3 btag CR
h_ttj_CR.Scale(h_ttj_SR.Integral()/h_ttj_CR.Integral())
#if do_shape==True: h_ttj=h_ttj_CR
#else             : h_ttj=h_ttj_SR
h_ttj=h_ttj_SR
h_ttj.Smooth()

#######ttbb
h_ttbb=infile.Get('tt+bb_sel0_h_m2j'+the_bin)
h_ttbb.Smooth()

# put proper norm
lumi = 30000000.
nbins = h_ttj.GetNbinsX()
nttj  = h_ttj.Integral( 0,nbins+1)*lumi
nttbb = h_ttbb.Integral(0,nbins+1)*lumi
nttbkgd=nttj+nttbb
h_ttj.Scale(nttj)
h_ttbb.Scale(nttbb)

## fits
h_ttbkg=h_ttj.Clone()
h_ttbkg.Add(h_ttbb)
myfit = r.TF1("myfit","pol5", low_x, high_x)
h_ttbkg.Fit("myfit","S","",low_x, high_x)
#h_ttbkg.Fit("myfit")

# extreme case
##############
#parl1_0 = 600.
#parl1_1 = 20.
#parl2_0 = 600.
#parl2_1 = -3.
# 1% case
##############
#parl1_0 = 600.
#parl1_1 = 5.
#parl2_0 = 600.
#parl2_1 = -0.75
# new cases
##############
percent = 5.*float(mode)
#
str_mode=""
if mode>0 : str_mode="_line"+str(int(percent))+"percent"
percent /= 100.
m_percent=-1.*percent
# the below parl[0]=(Y2-Y1)/(X2-X1)=(1-var_in_Y)/(100-0)
#parl1_1 = -2.*percent/100.
#parl1_0 =  1.+2.*percent
#parl2_1 = -2.*m_percent/100.
#parl2_0 =  1.+2.*m_percent
parl1_1 = percent/25.
parl1_0 = 1.-4.*percent
parl2_1 = m_percent/25.
parl2_0 = 1.-4.*m_percent

my_line1 = r.TF1("my_line1","pol1", low_x, high_x)
my_line1.SetParameters(parl1_0,parl1_1)

my_line2 = r.TF1("my_line2","pol1", low_x, high_x)
my_line2.SetParameters(parl2_0,parl2_1)

## hist from fits
h_ttbkg_fit=h_ttj.Clone()
h_ttbkg_fitup=h_ttj.Clone()
h_ttbkg_fitdo=h_ttj.Clone()
shift=5
for i_bin in xrange( 1, h_ttbkg_fit.GetNbinsX()+1 ):
  xval=h_ttbkg_fit.GetBinCenter(i_bin)
  bin_val = myfit.Eval(xval)
  if bin_val<0. : bin_val=0.
  h_ttbkg_fit.SetBinContent(i_bin, bin_val)
  # change shape with line
  ########################
  if do_shape==True:
    line1_val=my_line1.Eval(xval)
    if line1_val<0. : line1_val=0.
    line2_val=my_line2.Eval(xval)
    if line2_val<0. : line2_val=0.
    #
    h_ttbkg_fitup.SetBinContent( i_bin, bin_val * line1_val )
    h_ttbkg_fitdo.SetBinContent( i_bin, bin_val * line2_val )
  # shift
  ########################
  else :
    the_val = 0
    i_bin_shift = i_bin+shift
    if i_bin_shift>=1 and i_bin_shift<=h_ttbkg_fit.GetNbinsX():
      the_val = myfit.Eval(h_ttbkg_fit.GetBinCenter(i_bin_shift))
    if the_val<0. : the_val=0.
    h_ttbkg_fitup.SetBinContent(i_bin, the_val)
    #
    the_val = 0
    i_bin_shift = i_bin-shift
    if i_bin_shift>=1 and i_bin_shift<=h_ttbkg_fit.GetNbinsX():
      the_val = myfit.Eval(h_ttbkg_fit.GetBinCenter(i_bin_shift))
    if the_val<0. : the_val=0.
    h_ttbkg_fitdo.SetBinContent(i_bin, the_val)

Ninit=h_ttbkg_fit.Integral(low_x, high_x)
h_ttbkg_fit.SetLineWidth(3)
h_ttbkg_fit.SetLineColor(r.kGreen+3)
h_ttbkg.SetLineColor(r.kBlack)
#
Nfitup=h_ttbkg_fitup.Integral(low_x, high_x)
#if do_shape==True: h_ttbkg_fitup.Scale(Ninit/Nfitup)
h_ttbkg_fitup.SetLineWidth(3)
h_ttbkg_fitup.SetLineColor(r.kRed)
#
Nfitdo=h_ttbkg_fitdo.Integral(low_x, high_x)
#if do_shape==True: h_ttbkg_fitdo.Scale(Ninit/Nfitdo)
h_ttbkg_fitdo.SetLineWidth(3)
h_ttbkg_fitdo.SetLineColor(r.kBlue)

# preserve norm
h_ttbkg_fitup.Scale(h_ttbkg_fit.Integral( 0,nbins+1)/h_ttbkg_fitup.Integral( 0,nbins+1))
h_ttbkg_fitdo.Scale(h_ttbkg_fit.Integral( 0,nbins+1)/h_ttbkg_fitdo.Integral( 0,nbins+1))

r.gStyle.SetOptStat(0)

h_ttbkg_fitdo.GetXaxis().SetRangeUser(low_x, high_x)
h_ttbkg_fitdo.SetTitle("")
c = r.TCanvas("plot", "plot", 800, 800)
# get max
maxi=max(h_ttbkg_fitdo.GetMaximum(),h_ttbkg_fitup.GetMaximum())
h_ttbkg_fitdo.SetMaximum(maxi*1.05)
#
h_ttbkg_fitdo.Draw()
h_ttbkg_fitup.Draw("same")
h_ttbkg.Draw("same")
h_ttbkg_fit.Draw("same")
c.SaveAs("check_fit"+str_mode+".eps")

## ratio
h_ratio_up=h_ttbkg_fitup.Clone()
h_ratio_up.Add(h_ttbkg_fit,-1.)
h_ratio_up.Divide(h_ttbkg_fit)
#
h_ratio_do=h_ttbkg_fitdo.Clone()
h_ratio_do.Add(h_ttbkg_fit,-1.)
h_ratio_do.Divide(h_ttbkg_fit)

#h_ratio_up.GetXaxis().SetRangeUser(50., high_x)
maxi=max(h_ratio_up.GetMaximum(),h_ratio_do.GetMaximum())
mini=min(h_ratio_up.GetMinimum(),h_ratio_do.GetMinimum())
h_ratio_up.SetMinimum(mini)
h_ratio_up.SetMaximum(maxi)
h_ratio_up.SetTitle("")
c2 = r.TCanvas("plot1", "plot1", 800, 800)
h_ratio_up.Draw()
h_ratio_do.Draw("same")
c2.SaveAs("check_fit_ratio"+str_mode+".eps")

#print "h="+str(h_ttbkg_fit.Integral(low_x, high_x))
#print "hdo="+str(h_ttbkg_fitdo.Integral(low_x, high_x))
#print "hup="+str(h_ttbkg_fitup.Integral(low_x, high_x))

