import sys
import ROOT as r
infile = r.TFile.Open('/eos/experiment/fcc/hh/analyses/Higgs/ttH/FlatTreeAnalyzer_outputs/fcc_v02/May2018_highstat_prod/root_ttH/histos.root')

# to rebin need to recreate the histogram
Rebin=1 # 150 bins

# several histos with different binning are in input
#the_bin = ''      # 15 bins
#the_bin = '_l'    # 30 bins
#the_bin = '_l60'  # 60 bins
#the_bin = '_l90'  # 90 bins
#the_bin = '_l120' # 120 bins
the_bin = '_l150' # 150 bins

def Sign(x):
 return abs(x) == x

##########
## MODE ##
##########
if len(sys.argv)>1: mode = int(sys.argv[1])
else : mode = 0
# 0 = alpha stat
# 1 = alpha sys, bkg +10% scale
# 2 = alpha sys, bkg -10% scale
# 3 = alpha sys, bkgd shape from CR
# 4 = alpha sys, fit of bkgd shape from CR -> err FITup
# 5 = alpha sys, fit of bkgd shape from CR -> err FITdo
# 6 = alpha sys, fit of bkgd shape from CR -> err FITup 1%
# 7 = alpha sys, fit of bkgd shape from CR -> err FITdo 1%
#  8 = alpha sys, fit of bkgd shape from SR -> shift +5 bins
#  9 = alpha sys, fit of bkgd shape from SR -> shift -5 bins
# 10 = alpha sys, fit of bkgd shape from SR -> shift +4 bins
# 11 = alpha sys, fit of bkgd shape from SR -> shift -4 bins
# 12 = alpha sys, fit of bkgd shape from SR -> shift +3 bins
# 13 = alpha sys, fit of bkgd shape from SR -> shift -3 bins
# 14 = alpha sys, fit of bkgd shape from SR -> shift +2 bins
# 15 = alpha sys, fit of bkgd shape from SR -> shift -2 bins
# 16 = alpha sys, fit of bkgd shape from SR -> shift +1 bins
# 17 = alpha sys, fit of bkgd shape from SR -> shift -1 bins

## if time later
#  = alpha sys, JESup
#  = alpha sys, JESdo
if mode > 17 :
  print "mode="+str(mode)+" not supported -> check !!"
  quit()

def makePseudoExp(p_tth, p_ttz, p_bkg, sig, alpha, ntth, nttz, nbkg, alpha_val, alpha_err):
 # generate datasets

    print '================================================================================================='

    gen_tth = p_tth.generate(r.RooArgSet(x), ntth, r.RooFit.Extended())
    gen_ttz = p_ttz.generate(r.RooArgSet(x), nttz, r.RooFit.Extended())
    gen_bkg = p_bkg.generate(r.RooArgSet(x), nbkg, r.RooFit.Extended())

    d_ttcomb = gen_tth
    d_ttcomb.append(gen_ttz)
    d_ttcomb.append(gen_bkg)
    sig.fitTo(d_ttcomb,r.RooFit.SumW2Error(False),r.RooFit.PrintLevel(-1))
    print alpha.getError(), alpha.getVal()
    alpha.Print()
    alpha_err.Fill(alpha.getError())
    alpha_val.Fill(alpha.getVal())

    #ratio = (1-alpha.getVal())/(alpha.getVal())
    #ratio_err = alpha.getError()
    #print ratio, ratio_err
    #alpha_err.Fill(ratio_err)
    #alpha_val.Fill(ratio)


low_x=50
high_x=300
x = r.RooRealVar("x", "mjj", low_x, high_x)
frame = x.frame(r.RooFit.Title("sig+bkgd"))

#######ttH
h_tth=infile.Get('ttH_sel3_h_mjj'+the_bin)
h_tth.Rebin(Rebin)
h_tth.Smooth()
d_tth = r.RooDataHist("d_tth", "d_tth", r.RooArgList(x),r.RooFit.Import(h_tth))
p_tth = r.RooHistPdf("p_tth", "p_tth", r.RooArgSet(x),d_tth)
p_tth.plotOn(frame, r.RooFit.LineColor(r.kRed) )

#######ttZ
h_ttz=infile.Get('ttZ_sel3_h_mjj'+the_bin)
h_ttz.Rebin(Rebin)
h_ttz.Smooth()
d_ttz = r.RooDataHist("d_ttz", "dttz", r.RooArgList(x),r.RooFit.Import(h_ttz))
p_ttz = r.RooHistPdf("p_ttz", "p_ttz", r.RooArgSet(x),d_ttz)
p_ttz.plotOn(frame, r.RooFit.LineColor(r.kOrange) )

#######ttj
h_ttj_SR=infile.Get('tt+jets_sel3_h_mjj'+the_bin) # >=4 btag
h_ttj_CR=infile.Get('tt+jets_sel4_h_mjj'+the_bin) # <4 btag CR
# -> available in next round of plots
#h_ttj_CR=infile.Get('tt+jets_sel5_h_mjj'+the_bin) # <3 btag CR
h_ttj_CR.Scale(h_ttj_SR.Integral()/h_ttj_CR.Integral())
#
h_ttj=h_ttj_SR
if mode>=3 and mode<=7: h_ttj=h_ttj_CR
h_ttj.Rebin(Rebin)
h_ttj.Smooth()
d_ttj = r.RooDataHist("d_ttj", "dttj", r.RooArgList(x),r.RooFit.Import(h_ttj))
p_ttj = r.RooHistPdf("p_ttj", "p_ttj", r.RooArgSet(x),d_ttj)
#p_ttj.plotOn(frame, r.RooFit.LineColor(r.kBlue) )

#######ttbb
h_ttbb=infile.Get('tt+bb_sel3_h_mjj'+the_bin)
h_ttbb.Rebin(Rebin)
h_ttbb.Smooth()
d_ttbb = r.RooDataHist("d_ttbb", "dttbb", r.RooArgList(x),r.RooFit.Import(h_ttbb))
p_ttbb = r.RooHistPdf("p_ttbb", "p_ttbb", r.RooArgSet(x),d_ttbb)
#p_ttbb.plotOn(frame, r.RooFit.LineColor(r.kViolet) )

# fit tot bkgd for syst
if mode>=4 and mode<=17:
  h_ttbkg=h_ttj.Clone()
  h_ttbkg.Add(h_ttbb)
  myfit = r.TF1("myfit","pol5", low_x, high_x)
  h_ttbkg.Fit("myfit","S","",low_x, high_x)
  #
  parl0 = 600.
  parl1 = 20.
  if mode==5: parl1 = -3.
  if mode==6: parl1 = 5.
  if mode==7: parl1 = -0.75
  my_line = r.TF1("my_line","pol1", low_x, high_x)
  my_line.SetParameters(parl0,parl1)
  h_ttbkg_fit=h_ttj.Clone()
  h_ttbkg_fiterr=h_ttj.Clone()
  for i_bin in xrange( 1, h_ttbkg_fit.GetNbinsX()+1 ):
    bin_val = myfit.Eval(h_ttbkg_fit.GetBinCenter(i_bin))
    h_ttbkg_fit.SetBinContent(i_bin, bin_val)
    # change shape with line
    if mode<=7:
      the_val = my_line.Eval(h_ttbkg_fit.GetBinCenter(i_bin))
      if the_val<0. : the_val=0.
      bin_valerr = bin_val * the_val
      h_ttbkg_fiterr.SetBinContent(i_bin, bin_valerr)
    else:
      shift=0
      if mode==8 : shift=5
      if mode==9 : shift=-5
      if mode==10: shift=4
      if mode==11: shift=-4
      if mode==12: shift=3
      if mode==13: shift=-3
      if mode==14: shift=2
      if mode==15: shift=-2
      if mode==16: shift=1
      if mode==17: shift=-1
      #
      the_val = 0
      i_bin_shift = i_bin-shift
      if i_bin_shift>=1 and i_bin_shift<=h_ttbkg_fit.GetNbinsX():
        the_val = myfit.Eval(h_ttbkg_fit.GetBinCenter(i_bin_shift))
      if the_val<0. : the_val=0.
      h_ttbkg_fiterr.SetBinContent(i_bin, the_val)

  Ninit=h_ttbkg_fit.Integral(low_x, high_x)
  Nfiterr=h_ttbkg_fiterr.Integral(low_x, high_x)
  if mode<=7: h_ttbkg_fiterr.Scale(Ninit/Nfiterr)
  #
  d_ttbkg_fit = r.RooDataHist("d_ttbb", "dttbb", r.RooArgList(x),r.RooFit.Import(h_ttbkg_fiterr))
  p_ttbkg_fit = r.RooHistPdf("p_ttbb", "p_ttbb", r.RooArgSet(x),d_ttbkg_fit)

# add pdfs

ntth  = 209533.
nttz  = 109286.
nttj  = 488033.
nttbb = 1604772.
#
if mode==1 :
  nttj*=1.1
  nttbb*=1.1
if mode==2 :
  nttj*=0.9
  nttbb*=0.9
#
nsig = nttz+ntth
nbkg = nttbb+nttj
#
for_alpha = nttz/ntth
for_beta  = nttj/nttbb
for_sigFrac = nsig/(nsig+nbkg)
#
alpha = r.RooRealVar("alpha", "fraction of component in signal", for_alpha, 0., 1.)
#alpha.setConstant(True)
sig = r.RooAddPdf("sig", "Signal", r.RooArgList(p_tth, p_ttz),r.RooArgList(alpha))
#
beta = r.RooRealVar("beta", "background parameter", for_beta, 0., 1.)
beta.setConstant(True)
if mode>=4 and mode<=17:
  bkg = p_ttbkg_fit
else:
  bkg = r.RooAddPdf("bkg", "Background", r.RooArgList(p_ttj, p_ttbb),r.RooArgList(beta))
bkg.plotOn(frame, r.RooFit.LineColor(r.kBlue) )
#
sigFrac = r.RooRealVar("sigFrac", "fraction of signal in the tot PDF", for_sigFrac, 0., 1.)
sigFrac.setConstant(True)
sigBkg = r.RooAddPdf("sigBkg", "Signal+Background", r.RooArgList(sig,bkg),r.RooArgList(sigFrac))

extra = '_STAT'
if mode==1: extra = '_SCALEup'
if mode==2: extra = '_SCALEdo'
if mode==3: extra = '_SHAPECR'
if mode==4: extra = '_FITCRup'
if mode==5: extra = '_FITCRdo'
if mode==6: extra = '_FITCR1percentup'
if mode==7: extra = '_FITCR1percentdo'
if mode==8 : extra = '_SHIFT5SRup'
if mode==9 : extra = '_SHIFT5SRdo'
if mode==10: extra = '_SHIFT4SRup'
if mode==11: extra = '_SHIFT4SRdo'
if mode==12: extra = '_SHIFT3SRup'
if mode==13: extra = '_SHIFT3SRdo'
if mode==14: extra = '_SHIFT2SRup'
if mode==15: extra = '_SHIFT2SRdo'
if mode==16: extra = '_SHIFT1SRup'
if mode==17: extra = '_SHIFT1SRdo'

alpha_val = r.TH1F("alpha_val"+extra, "alpha_val"+extra, 500, 0.5, 0.6)
alpha_err = r.TH1F("alpha_err"+extra, "alpha_err"+extra, 500, 0.0045, 0.055)


for i in xrange(1000):
    makePseudoExp(p_tth, p_ttz, bkg, sigBkg, alpha, int(ntth), int(nttz), int(nbkg), alpha_val, alpha_err)


outfile = r.TFile('tth_fit_'+str(mode)+'.root','RECREATE')
alpha_val.Write()
alpha_err.Write()

c = r.TCanvas("plot", "plot", 800, 800)
frame.GetYaxis().SetTitleOffset(1.4)
frame.Draw()
c.SaveAs("sig_bkg_for_fit"+extra+".eps")
