import sys
import ROOT as r
import copy

######################
# 1st stable results (without sig/d_ttcomb FitTo inversion bug)
# http://djamin.web.cern.ch/djamin/FCC/20180403_tth_boosted/high_stat/tth_fit_model.pdf
######################

quiet_mode=True
#quiet_mode=False

do_RooFit=True
#do_RooFit=False

# RooFit silent mode
if quiet_mode==True: r.RooMsgService.instance().setGlobalKillBelow(r.RooFit.WARNING)

# sel = [0,5]
infile = r.TFile.Open('/eos/experiment/fcc/hh/analyses/Higgs/ttH/FlatTreeAnalyzer_outputs/fcc_v02/May2018_highstat_prod/good_sel_2D_optim_tail_removal/root_ttH/histos.root')
# sel = [0,3]
#infile = r.TFile.Open('/eos/experiment/fcc/hh/analyses/Higgs/ttH/FlatTreeAnalyzer_outputs/fcc_v02/May2018_highstat_prod/good_sel_ttz_optim_tail_removal/root_ttH/histos.root')

######################
#####   PARAMS   #####
######################

# smooth histos for fit
#do_Smooth=False
do_Smooth=True # good

# several histos with different binning are in input
#the_bin = ''      # 15 bins
#the_bin = '_l'    # 30 bins
#the_bin = '_l60'  # 60 bins
#the_bin = '_l90'  # 90 bins
#the_bin = '_l120' # 120 bins
the_bin = '_l150' # 150 bins -> good

use_fit=True
#use_fit=False

#the_var = 'h_mjj' # old
the_var = 'h_m2j' # good

#the_sel = 4 # init good
the_sel = 0 # for file with 2D cut tests

the_fit_func = "pol6" # good

low_x=50
high_x=250
## full range
#low_x=0
#high_x=300
## test to avoid tail effects
#low_x=60
#high_x=140

fitlow_x=45
fithigh_x=300

lumi = 30000000.

######################

def Sign(x):
 return abs(x) == x

##########
## MODE ##
##########
if len(sys.argv)>1: mode = int(sys.argv[1])
else : mode = 0
# 0 = alpha stat, fit of bkgd shape from SR
########
# 1 = alpha sys, fit of bkgd shape from SR -> bkg +10% scale
# 2 = alpha sys, fit of bkgd shape from SR -> bkg -10% scale
########
# 3 = alpha sys, fit of bkgd shape from CR
########
# 4  = alpha sys, fit of bkgd shape from SR -> err shape by  0%
# 5  = alpha sys, fit of bkgd shape from SR -> err shape by +1%
# 6  = alpha sys, fit of bkgd shape from SR -> err shape by -1%
# 7  = alpha sys, fit of bkgd shape from SR -> err shape by +2%
# 8  = alpha sys, fit of bkgd shape from SR -> err shape by -2%
# 9  = alpha sys, fit of bkgd shape from SR -> err shape by +3%
# 10 = alpha sys, fit of bkgd shape from SR -> err shape by -3%
# 11 = alpha sys, fit of bkgd shape from SR -> err shape by +4%
# 12 = alpha sys, fit of bkgd shape from SR -> err shape by -4%
# 13 = alpha sys, fit of bkgd shape from SR -> err shape by +5%
# 14 = alpha sys, fit of bkgd shape from SR -> err shape by -5%
# 15 = alpha sys, fit of bkgd shape from SR -> err shape by +6%
# 16 = alpha sys, fit of bkgd shape from SR -> err shape by -6%
########
# 17 = alpha sys, fit of bkgd shape from SR -> shift +2 bins
# 18 = alpha sys, fit of bkgd shape from SR -> shift -2 bins
# 19 = alpha sys, fit of bkgd shape from SR -> shift +1 bins
# 20 = alpha sys, fit of bkgd shape from SR -> shift -1 bins

if mode > 20 :
  print "mode="+str(mode)+" not supported -> check !!"
  quit()

def makePseudoExp(sigBkg, sigBkg_modif, ntth, nttz, nbkg_modif, alpha, alpha_val, alpha_err, beta, beta_val, sigFrac, sigFrac_val, beta_modif, beta_modif_val):

    if quiet_mode==False: print '================================================================================================='

    # keep alpha
    alpha.setVal(nttz/ntth)

    # generate datasets + form template
    #d_ttcomb = sigBkg_modif.generate(r.RooArgSet(x), int(nbkg_modif+ntth+nttz), r.RooFit.Extended())
    d_ttcomb = sigBkg_modif.generateBinned(r.RooArgSet(x), int(nbkg_modif+ntth+nttz), r.RooFit.Extended())

    ratio = 0.
    ratio_err = 0.
    ratio_beta = 0.
    ratio_beta_modif = 0.

    #########
    # RooFit
    #########
    if do_RooFit==True :
      sigBkg.fitTo(d_ttcomb,r.RooFit.SumW2Error(False),r.RooFit.PrintLevel(-1))
      if quiet_mode==False: print alpha.getVal(), alpha.getError()
      if quiet_mode==False: alpha.Print()
      # invert alpha
      ratio = 1./alpha.getVal()
      ratio_err = alpha.getError()/alpha.getVal()
      ratio_beta = 1./beta.getVal()
      ratio_beta_modif = 1./beta_modif.getVal()
      if quiet_mode==False: print "alpha=",alpha.getVal(),", beta=",beta.getVal(),", beta_modif=",beta_modif.getVal(),", sigFrac=",sigFrac.getVal()

    #########
    # RooStat
    #########
    else :
      w = r.RooWorkspace("w")
      getattr(w,'import')(sigBkg)
      getattr(w,'import')(d_ttcomb)
      #
      model = r.RooStats.ModelConfig()
      model.SetWorkspace(w)
      model.SetPdf("sigBkg")
      #
      w_alpha = w.var("alpha")
      poi = r.RooArgSet(w_alpha)
      #
      plc = r.RooStats.ProfileLikelihoodCalculator(d_ttcomb,model)
      plc.SetParameters(poi)
      plc.SetConfidenceLevel(0.68)
      #
      plInt = plc.GetInterval()
      alpha_low  = plInt.LowerLimit(w_alpha)
      alpha_high = plInt.UpperLimit(w_alpha)
      # invert alpha
      mean_alpha = (alpha_low+alpha_high)/2.
      ratio = 1./mean_alpha
      ratio_err = w_alpha.getError()/mean_alpha
      if quiet_mode==False: print alpha_low, alpha_high, mean_alpha, w_alpha.getError()

    # fill alpha
    alpha_val.Fill(ratio)
    alpha_err.Fill(ratio_err)
    beta_val.Fill(ratio_beta)
    beta_modif_val.Fill(ratio_beta_modif)
    sigFrac_val.Fill(sigFrac.getVal())
    if quiet_mode==False: print ratio, ratio_err, ratio_beta, ratio_beta_modif, sigFrac.getVal()

def Fit_Fill(h, h_fit):
  fit = r.TF1("fit",the_fit_func, low_x, high_x)
  #option_draw="S"
  option_draw=""
  if quiet_mode==True: option_draw+="QN0"
  h.Fit("fit",option_draw,"",fitlow_x, fithigh_x)
  # re-fill histo
  for i_bin in xrange( 1, h_fit.GetNbinsX()+1 ):
    bin_val = fit.Eval(h_fit.GetBinCenter(i_bin))
    if bin_val<0. : bin_val=0.
    h_fit.SetBinContent(i_bin, bin_val)
  return h_fit

def modif_line(h, h_line):

  percent = 1.
  if mode==4  : percent =  0.
  if mode==5  : percent =  1.
  if mode==6  : percent = -1.
  if mode==7  : percent =  2.
  if mode==8  : percent = -2.
  if mode==9  : percent =  3.
  if mode==10 : percent = -3.
  if mode==11 : percent =  4.
  if mode==12 : percent = -4.
  if mode==13 : percent =  5.
  if mode==14 : percent = -5.
  if mode==15 : percent =  6.
  if mode==16 : percent = -6.
  percent /= 100.
  #
  # the below parl[0]=(Y2-Y1)/(X2-X1)=(1-var_in_Y)/(100-0)
  parl = [percent/25., 1.-4.*percent]
  #
  my_line = r.TF1("my_line","pol1", low_x, high_x)
  my_line.SetParameters(parl[1],parl[0])
  for i_bin in xrange( 1, h.GetNbinsX()+1 ):
    bin_val = h.GetBinContent(i_bin)
    the_val = my_line.Eval(h.GetBinCenter(i_bin))
    h_line.SetBinContent(i_bin, bin_val*the_val)

def modif_shift(h, h_shift):

    shift=0
    if mode==17: shift=2
    if mode==18: shift=-2
    if mode==19: shift=1
    if mode==20: shift=-1
    #
    for i_bin in xrange( 1, h.GetNbinsX()+1 ):
      the_val = 0
      i_bin_shift = i_bin-shift
      if i_bin_shift>0 and i_bin_shift<=h.GetNbinsX(): the_val = h.GetBinContent(i_bin_shift)
      h_shift.SetBinContent(i_bin, the_val)


##################
# return to main

x = r.RooRealVar("x", "mjj", low_x, high_x)
frame = x.frame(r.RooFit.Title("sig+bkgd"))

##################
#######ttH
h_tth=infile.Get('ttH_sel'+str(the_sel)+'_'+the_var+the_bin)
h_tth.Scale(lumi)
if do_Smooth==True : h_tth.Smooth()
d_tth = r.RooDataHist("d_tth", "d_tth", r.RooArgList(x),r.RooFit.Import(h_tth))
p_tth = r.RooHistPdf("p_tth", "p_tth", r.RooArgSet(x),d_tth)
#p_tth.plotOn(frame, r.RooFit.LineColor(r.kRed) )

##################
#######ttZ
h_ttz=infile.Get('ttZ_sel'+str(the_sel)+'_'+the_var+the_bin)
h_ttz.Scale(lumi)
if do_Smooth==True : h_ttz.Smooth()
d_ttz = r.RooDataHist("d_ttz", "dttz", r.RooArgList(x),r.RooFit.Import(h_ttz))
p_ttz = r.RooHistPdf("p_ttz", "p_ttz", r.RooArgSet(x),d_ttz)
#p_ttz.plotOn(frame, r.RooFit.LineColor(r.kViolet) )

# scale variation of bkgd
percent=0.1 # 10%

##################
#######ttj
h_ttj_SR=infile.Get('tt+jets_sel'+str(the_sel)+'_'+the_var+the_bin) # >=4 btag
h_ttj_CR=infile.Get('tt+jets_sel'+str(the_sel)+'_'+the_var+the_bin) # tmp fix
#h_ttj_CR=infile.Get('tt+jets_sel'+str(the_sel+1)+'_'+the_var+the_bin) # <4 btag CR
# -> available in next round of plots
#h_ttj_CR=infile.Get('tt+jets_sel'+str(the_sel+2)+'_'+the_var+the_bin) # <3 btag CR
h_ttj_CR.Scale(h_ttj_SR.Integral()/h_ttj_CR.Integral())
#
h_ttj=h_ttj_SR
if mode==3: h_ttj=h_ttj_CR
# smooth
if do_Smooth==True : h_ttj.Smooth()
# fit
#h_ttj_fit=h_ttj.Clone()
h_ttj_fit=copy.deepcopy(h_ttj)
if use_fit==True: Fit_Fill(h_ttj, h_ttj_fit)
h_ttj_fit.Scale(lumi)
# nominal shape
d_ttj = r.RooDataHist("d_ttj", "dttj", r.RooArgList(x),r.RooFit.Import(h_ttj_fit))
p_ttj = r.RooHistPdf("p_ttj", "p_ttj", r.RooArgSet(x),d_ttj)
# compute shape modif
#h_ttj_modif=h_ttj_fit.Clone()
h_ttj_modif=copy.deepcopy(h_ttj_fit)
if mode==1 : h_ttj_modif.Scale(1.+percent)
if mode==2 : h_ttj_modif.Scale(1.-percent)
if mode>=4  and mode<=16: modif_line(h_ttj_fit, h_ttj_modif)
if mode>=17 and mode<=20: modif_shift(h_ttj_fit, h_ttj_modif)
# modified shape
d_ttj_modif = r.RooDataHist("d_ttj_modif", "dttj_modif", r.RooArgList(x),r.RooFit.Import(h_ttj_modif))
p_ttj_modif = r.RooHistPdf("p_ttj_modif", "p_ttj_modif", r.RooArgSet(x),d_ttj_modif)
#p_ttj_modif.plotOn(frame, r.RooFit.LineColor(r.kBlue+1) )

##################
#######ttbb
h_ttbb=infile.Get('tt+bb_sel'+str(the_sel)+'_'+the_var+the_bin)
# smooth
if do_Smooth==True : h_ttbb.Smooth()
# fit
h_ttbb_fit=copy.deepcopy(h_ttbb)
if use_fit==True: Fit_Fill(h_ttbb, h_ttbb_fit)
h_ttbb_fit.Scale(lumi)
# nominal shape
d_ttbb = r.RooDataHist("d_ttbb", "dttbb", r.RooArgList(x),r.RooFit.Import(h_ttbb_fit))
p_ttbb = r.RooHistPdf("p_ttbb", "p_ttbb", r.RooArgSet(x),d_ttbb)
# compute shape modif
h_ttbb_modif=copy.deepcopy(h_ttbb_fit)
if mode==1 : h_ttbb_modif.Scale(1.+percent)
if mode==2 : h_ttbb_modif.Scale(1.-percent)
if mode>=4  and mode<=16: modif_line(h_ttbb_fit, h_ttbb_modif)
if mode>=17 and mode<=20: modif_shift(h_ttbb_fit, h_ttbb_modif)
# modified shape
d_ttbb_modif = r.RooDataHist("d_ttbb_modif", "dttbb_modif", r.RooArgList(x),r.RooFit.Import(h_ttbb_modif))
p_ttbb_modif = r.RooHistPdf("p_ttbb_modif", "p_ttbb_modif", r.RooArgSet(x),d_ttbb_modif)
#p_ttbb_modif.plotOn(frame, r.RooFit.LineColor(r.kGreen+2) )


##################
# add pdfs
nbins = h_tth.GetNbinsX()
x0   = 0
xmax = nbins+1
#
ntth        = h_tth.Integral(x0, xmax)
nttz        = h_ttz.Integral(x0, xmax) 
nttj        = h_ttj_fit.Integral(x0, xmax)
nttbb       = h_ttbb_fit.Integral(x0, xmax)
nttj_modif  = h_ttj_modif.Integral(x0, xmax)
nttbb_modif = h_ttbb_modif.Integral(x0, xmax)
#
nsig       = nttz+ntth
nbkg       = nttbb+nttj
nbkg_modif = nttbb_modif+nttj_modif
#
alpha_expected         = ntth/nttz
beta_expected          = nttbb/nttj
beta_modif_expected    = nttbb_modif/nttj_modif
sigFrac_expected       = nsig/(nsig+nbkg)
sigFrac_expected_modif = nsig/(nsig+nbkg_modif)
#
for_alpha         = 1./alpha_expected
for_beta          = 1./beta_expected
for_beta_modif    = 1./beta_modif_expected
for_sigFrac       = sigFrac_expected
for_sigFrac_modif = sigFrac_expected_modif

if quiet_mode==False:
  print "#################\n expected from yields :"
  print "ntth=",ntth,"/ nttz=",nttz,"-> for_alpha=",for_alpha,", alpha=",alpha_expected
  print "nttbb=",nttbb,"/ nttj=",nttj,"-> for_beta=",for_beta,", beta=",beta_expected
  print "nttbb_modif=",nttbb_modif,"/ nttj_modif=",nttj_modif,"-> for_beta_modif=",for_beta_modif,", beta_modif=",beta_modif_expected
  print "nsig=",nsig,"/ nbkg=",nbkg,"-> sigFrac=",sigFrac_expected


##################
alpha = r.RooRealVar("alpha", "fraction of component in signal", for_alpha, 0., 1.)
#alpha.setConstant(True)
sig = r.RooAddPdf("sig", "Signal", r.RooArgList(p_ttz, p_tth),r.RooArgList(alpha))
sig.plotOn(frame, r.RooFit.LineColor(r.kRed+1) )

##################
beta = r.RooRealVar("beta", "background parameter", for_beta, 0., 1.)
beta.setConstant(True)
bkg = r.RooAddPdf("bkg", "Background", r.RooArgList(p_ttj, p_ttbb),r.RooArgList(beta))
#bkg.plotOn(frame, r.RooFit.LineColor(r.kOrange+1) )
#
beta_modif = r.RooRealVar("beta_modif", "background modified parameter", for_beta_modif, 0., 1.)
beta_modif.setConstant(True)
bkg_modif = r.RooAddPdf("bkg_modif", "Background_modif", r.RooArgList(p_ttj_modif, p_ttbb_modif),r.RooArgList(beta_modif))
#bkg_modif.plotOn(frame, r.RooFit.LineColor(r.kBlack) )

##################
sigFrac = r.RooRealVar("sigFrac", "fraction of signal in the tot PDF", for_sigFrac, 0., 1.)
sigFrac.setConstant(True)
sigBkg = r.RooAddPdf("sigBkg", "Signal+Background", r.RooArgList(sig,bkg),r.RooArgList(sigFrac))
#
sigFrac_modif = r.RooRealVar("sigFrac_modif", "fraction of signal in the tot PDF modified", for_sigFrac_modif, 0., 1.)
sigFrac_modif.setConstant(True)
sigBkg_modif = r.RooAddPdf("sigBkg_modif", "Signal+Background_modif", r.RooArgList(sig,bkg_modif),r.RooArgList(sigFrac_modif))
#
sigBkg.plotOn(frame, r.RooFit.LineColor(r.kGreen+3),  r.RooFit.LineStyle(r.kDashed) )
sigBkg_modif.plotOn(frame, r.RooFit.LineColor(r.kBlue) )

extra = '_STAT'
if mode==1 : extra = '_SCALEup'
if mode==2 : extra = '_SCALEdo'
if mode==3 : extra = '_SHAPECR'
if mode==4 : extra = '_FITSR0'
if mode==5 : extra = '_FITSR1up'
if mode==6 : extra = '_FITSR1do'
if mode==7 : extra = '_FITSR2up'
if mode==8 : extra = '_FITSR2do'
if mode==9 : extra = '_FITSR3up'
if mode==10: extra = '_FITSR3do'
if mode==11: extra = '_FITSR4up'
if mode==12: extra = '_FITSR4do'
if mode==13: extra = '_FITSR5up'
if mode==14: extra = '_FITSR5do'
if mode==15: extra = '_FITSR6up'
if mode==16: extra = '_FITSR6do'
if mode==17: extra = '_SHIFT2SRup'
if mode==18: extra = '_SHIFT2SRdo'
if mode==19: extra = '_SHIFT1SRup'
if mode==20: extra = '_SHIFT1SRdo'

alpha_val = r.TH1F("alpha_val"+extra, "alpha_val"+extra, 1000, 0.0, 100.0)
alpha_err = r.TH1F("alpha_err"+extra, "alpha_err"+extra, 500, 0.0, 1.0)
beta_val = r.TH1F("beta_val"+extra, "beta_val"+extra, 1000, 0.0, 100.0)
beta_modif_val = r.TH1F("beta_modif_val"+extra, "beta_modif_val"+extra, 1000, 0.0, 100.0)
sigFrac_val = r.TH1F("sigFrac_val"+extra, "sigFrac_val"+extra, 1000, 0.0, 100.0)

if quiet_mode==False: print "before loop : alpha=",alpha.getVal(),", beta=",beta.getVal(),", beta_modif=",beta_modif.getVal(),", sigFrac=",sigFrac.getVal()

n_pseudo = 1
if do_RooFit==True: n_pseudo = 1000
for i in xrange(n_pseudo):
    makePseudoExp(sigBkg, sigBkg_modif, ntth, nttz, nbkg_modif, alpha, alpha_val, alpha_err, beta, beta_val, sigFrac, sigFrac_val, beta_modif, beta_modif_val)


outfile = r.TFile('tth_fit_'+str(mode)+'.root','RECREATE')

if mode==0:
  alpha_exp = r.TH1F("alpha_exp"+extra, "alpha_exp"+extra, 1000, 0.0, 100.0)
  alpha_exp.Fill(alpha_expected)
  alpha_exp.Write()
  beta_exp = r.TH1F("beta_exp"+extra, "beta_exp"+extra, 1000, 0.0, 100.0)
  beta_exp.Fill(beta_expected)
  beta_exp.Write()
  beta_modif_exp = r.TH1F("beta_modif_exp"+extra, "beta_modif_exp"+extra, 1000, 0.0, 100.0)
  beta_modif_exp.Fill(beta_modif_expected)
  beta_modif_exp.Write()
  sigFrac_exp = r.TH1F("sigFrac_exp"+extra, "sigFrac_exp"+extra, 1000, 0.0, 100.0)
  sigFrac_exp.Fill(sigFrac_expected)
  sigFrac_exp.Write()
alpha_val.Write()
alpha_err.Write()
beta_val.Write()
beta_modif_val.Write()
sigFrac_val.Write()

c = r.TCanvas("plot", "plot", 800, 800)
if quiet_mode==True: c.SetBatch(r.kTRUE)
frame.GetYaxis().SetTitleOffset(1.4)
frame.Draw()
c.SaveAs("sig_bkg_for_fit"+extra+".eps")

# final print
print "------------> measured :"
print "alpha =",alpha_val.GetMean(),",",alpha_err.GetMean()
print "beta =",beta_val.GetMean(),", beta_modif =",beta_modif_val.GetMean(),", sigFrac =",sigFrac_val.GetMean()
print "mode =",mode
