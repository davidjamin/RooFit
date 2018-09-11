import sys
import ROOT as r

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
the_sel = 0

the_fit_func = "pol6" # good

low_x=50
high_x=250

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
# 4 = alpha sys, fit of bkgd shape from SR -> err shape by 0%
# 5 = alpha sys, fit of bkgd shape from SR -> err shape by +0.5%
# 6 = alpha sys, fit of bkgd shape from SR -> err shape by -0.5%
# 7 = alpha sys, fit of bkgd shape from SR -> err shape by +1.0%
# 8 = alpha sys, fit of bkgd shape from SR -> err shape by -1.0%
# 9 = alpha sys, fit of bkgd shape from SR -> err shape by +1.5%
# 10 = alpha sys, fit of bkgd shape from SR -> err shape by -1.5%
# 11 = alpha sys, fit of bkgd shape from SR -> err shape by +2.0%
# 12 = alpha sys, fit of bkgd shape from SR -> err shape by -2.0%
# 13 = alpha sys, fit of bkgd shape from SR -> err shape by +2.5%
# 14 = alpha sys, fit of bkgd shape from SR -> err shape by -2.5%
# 15 = alpha sys, fit of bkgd shape from SR -> err shape by +3.0%
# 16 = alpha sys, fit of bkgd shape from SR -> err shape by -3.0%
########
# 17 = alpha sys, fit of bkgd shape from SR -> shift +2 bins
# 18 = alpha sys, fit of bkgd shape from SR -> shift -2 bins
# 19 = alpha sys, fit of bkgd shape from SR -> shift +1 bins
# 20 = alpha sys, fit of bkgd shape from SR -> shift -1 bins

## if time later
#  = alpha sys, JESup
#  = alpha sys, JESdo
if mode > 20 :
  print "mode="+str(mode)+" not supported -> check !!"
  quit()

def makePseudoExp(p_tth, p_ttz, p_bkg_modif, sig, alpha, ntth, nttz, nbkg_modif, alpha_val, alpha_err, beta, beta_val, sigFrac, sigFrac_val):

    if quiet_mode==False: print '================================================================================================='

    # generate datasets
    gen_tth = p_tth.generate(r.RooArgSet(x), ntth, r.RooFit.Extended())
    gen_ttz = p_ttz.generate(r.RooArgSet(x), nttz, r.RooFit.Extended())
    gen_bkg_modif = p_bkg_modif.generate(r.RooArgSet(x), nbkg_modif, r.RooFit.Extended())

    # form template
    d_ttcomb = gen_tth
    d_ttcomb.append(gen_ttz)
    d_ttcomb.append(gen_bkg_modif) # comment here if you don't want bkgd


    ratio = 0.
    ratio_err = 0.
    ratio_beta = 0.

    #########
    # RooFit
    #########
    if do_RooFit==True :
      sig.fitTo(d_ttcomb,r.RooFit.SumW2Error(False),r.RooFit.PrintLevel(-1))
      #d_ttcomb.fitTo(sig,r.RooFit.SumW2Error(False),r.RooFit.PrintLevel(-1))
      if quiet_mode==False: print alpha.getVal(), alpha.getError()
      if quiet_mode==False: alpha.Print()
      # invert alpha
      ratio = (1.-alpha.getVal())/alpha.getVal()
      ratio_err = alpha.getError()/alpha.getVal()
      ratio_beta = (1.-beta.getVal())/beta.getVal()
      if quiet_mode==False: print "alpha=",alpha.getVal(),", beta=",beta.getVal(),", sigFrac=",sigFrac.getVal()

    #########
    # RooStat
    #########
    else :
      w = r.RooWorkspace("w")
      getattr(w,'import')(sig)
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
      ratio = (1.-mean_alpha)/mean_alpha
      ratio_err = w_alpha.getError()/mean_alpha
      if quiet_mode==False: print alpha_low, alpha_high, mean_alpha, w_alpha.getError()

    # fill alpha
    alpha_val.Fill(ratio)
    alpha_err.Fill(ratio_err)
    beta_val.Fill(ratio_beta)
    sigFrac_val.Fill(sigFrac.getVal())
    if quiet_mode==False: print ratio, ratio_err, ratio_beta, sigFrac

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
  if mode==4  : percent = 0.
  if mode==5  : percent = 0.5
  if mode==6  : percent = -0.5
  if mode==7  : percent = 1.
  if mode==8  : percent = -1.
  if mode==9 : percent = 1.5
  if mode==10 : percent = -1.5
  if mode==11 : percent = 2.
  if mode==12 : percent = -2.
  if mode==13 : percent = 2.5
  if mode==14 : percent = -2.5
  if mode==15 : percent = 3.
  if mode==16 : percent = -3.
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
p_tth.plotOn(frame, r.RooFit.LineColor(r.kRed) )

##################
#######ttZ
h_ttz=infile.Get('ttZ_sel'+str(the_sel)+'_'+the_var+the_bin)
h_ttz.Scale(lumi)
if do_Smooth==True : h_ttz.Smooth()
d_ttz = r.RooDataHist("d_ttz", "dttz", r.RooArgList(x),r.RooFit.Import(h_ttz))
p_ttz = r.RooHistPdf("p_ttz", "p_ttz", r.RooArgSet(x),d_ttz)
p_ttz.plotOn(frame, r.RooFit.LineColor(r.kViolet) )

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
h_ttj_fit=h_ttj.Clone()
if use_fit==True: Fit_Fill(h_ttj, h_ttj_fit)
h_ttj_fit.Scale(lumi)
# nominal shape
d_ttj = r.RooDataHist("d_ttj", "dttj", r.RooArgList(x),r.RooFit.Import(h_ttj_fit))
p_ttj = r.RooHistPdf("p_ttj", "p_ttj", r.RooArgSet(x),d_ttj)
# compute shape modif
h_ttj_modif=h_ttj_fit.Clone()
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
h_ttbb_fit=h_ttbb.Clone()
if use_fit==True: Fit_Fill(h_ttbb, h_ttbb_fit)
h_ttbb_fit.Scale(lumi)
# nominal shape
d_ttbb = r.RooDataHist("d_ttbb", "dttbb", r.RooArgList(x),r.RooFit.Import(h_ttbb_fit))
p_ttbb = r.RooHistPdf("p_ttbb", "p_ttbb", r.RooArgSet(x),d_ttbb)
# compute shape modif
h_ttbb_modif=h_ttbb_fit.Clone()
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
ntth  = h_tth.Integral( 0,nbins+1)
nttz  = h_ttz.Integral( 0,nbins+1) 
nttj  = h_ttj_fit.Integral( 0,nbins+1)
nttbb = h_ttbb_fit.Integral(0,nbins+1)
nttj_modif  = h_ttj_modif.Integral( 0,nbins+1)
nttbb_modif = h_ttbb_modif.Integral(0,nbins+1)
expected=ntth/nttz
#
nsig = nttz+ntth
nbkg = nttbb+nttj
nbkg_modif = nttbb_modif+nttj_modif
#
for_alpha = nttz/ntth
for_beta  = nttj/nttbb
for_beta_modif = nttj_modif/nttbb_modif
for_sigFrac = nsig/(nsig+nbkg)
for_sigFrac_modif = nsig/(nsig+nbkg_modif)
print "#################\n expected from yields :"
print "ntth=",ntth,"/ nttz=",nttz,"-> for_alpha=",for_alpha,", alpha=",ntth/nttz
print "nttbb=",nttbb,"/ nttj=",nttj,"-> for_beta=",for_beta,", beta=",nttbb/nttj
print "nttbb_modif=",nttbb_modif,"/ nttj_modif=",nttj_modif,"-> for_beta_modif=",for_beta_modif,", beta_modif=",nttbb_modif/nttj_modif
print "nsig=",nsig,"/ nbkg=",nbkg,"-> for_sigFrac=",for_sigFrac


##################
alpha = r.RooRealVar("alpha", "fraction of component in signal", for_alpha, 0., 1.)
#alpha.setConstant(True)
sig = r.RooAddPdf("sig", "Signal", r.RooArgList(p_ttz, p_tth),r.RooArgList(alpha))

##################
beta = r.RooRealVar("beta", "background parameter", for_beta, 0., 1.)
beta.setConstant(True)
bkg = r.RooAddPdf("bkg", "Background", r.RooArgList(p_ttj, p_ttbb),r.RooArgList(beta))
bkg.plotOn(frame, r.RooFit.LineColor(r.kOrange+1) )
#
beta_modif = r.RooRealVar("beta_modif", "background modified parameter", for_beta_modif, 0., 1.)
beta_modif.setConstant(True)
bkg_modif = r.RooAddPdf("bkg_modif", "Background_modif", r.RooArgList(p_ttj_modif, p_ttbb_modif),r.RooArgList(beta_modif))
bkg_modif.plotOn(frame, r.RooFit.LineColor(r.kBlack) )

##################
sigFrac = r.RooRealVar("sigFrac", "fraction of signal in the tot PDF", for_sigFrac, 0., 1.)
sigFrac.setConstant(True)
sigBkg = r.RooAddPdf("sigBkg", "Signal+Background", r.RooArgList(sig,bkg),r.RooArgList(sigFrac))
#
#sigFrac_modif = r.RooRealVar("sigFrac_modif", "fraction of signal in the tot PDF modified", for_sigFrac_modif, 0., 1.)
##sigFrac_modif.setConstant(True)
#sigBkg_modif = r.RooAddPdf("sigBkg_modif", "Signal+Background_modif", r.RooArgList(sig,bkg_modif),r.RooArgList(sigFrac_modif))

extra = '_STAT'
if mode==1 : extra = '_SCALEup'
if mode==2 : extra = '_SCALEdo'
if mode==3 : extra = '_SHAPECR'
if mode==4 : extra = '_FITSR0'
if mode==5 : extra = '_FITSR0.5up'
if mode==6 : extra = '_FITSR0.5do'
if mode==7 : extra = '_FITSR1up'
if mode==8 : extra = '_FITSR1do'
if mode==9 : extra = '_FITSR1.5up'
if mode==10: extra = '_FITSR1.5do'
if mode==11: extra = '_FITSR2up'
if mode==12: extra = '_FITSR2do'
if mode==13: extra = '_FITSR2.5up'
if mode==14: extra = '_FITSR2.5do'
if mode==15: extra = '_FITSR3up'
if mode==16: extra = '_FITSR3do'
if mode==17: extra = '_SHIFT2SRup'
if mode==18: extra = '_SHIFT2SRdo'
if mode==19: extra = '_SHIFT1SRup'
if mode==20: extra = '_SHIFT1SRdo'

alpha_val = r.TH1F("alpha_val"+extra, "alpha_val"+extra, 1000, 0.0, 100.0)
alpha_err = r.TH1F("alpha_err"+extra, "alpha_err"+extra, 500, 0.0, 1.0)
beta_val = r.TH1F("beta_val"+extra, "beta_val"+extra, 1000, 0.0, 100.0)
sigFrac_val = r.TH1F("sigFrac_val"+extra, "sigFrac_val"+extra, 1000, 0.0, 100.0)

n_pseudo = 1
if do_RooFit==True : n_pseudo = 1000
for i in xrange(n_pseudo):
    ## sigBkg = initial case
    makePseudoExp(p_tth, p_ttz, bkg_modif, sigBkg, alpha, int(ntth), int(nttz), int(nbkg_modif), alpha_val, alpha_err, beta, beta_val, sigFrac, sigFrac_val)


outfile = r.TFile('tth_fit_'+str(mode)+'.root','RECREATE')

if mode==0:
  alpha_exp = r.TH1F("alpha_exp"+extra, "alpha_exp"+extra, 1000, 0.0, 100.0)
  alpha_exp.Fill(expected)
  alpha_exp.Write()
alpha_val.Write()
alpha_err.Write()
beta_val.Write()
sigFrac_val.Write()

c = r.TCanvas("plot", "plot", 800, 800)
if quiet_mode==True: c.SetBatch(r.kTRUE)
frame.GetYaxis().SetTitleOffset(1.4)
frame.Draw()
c.SaveAs("sig_bkg_for_fit"+extra+".eps")

# final print
print "------------> measured :"
print "alpha =",alpha_val.GetMean(),",",alpha_err.GetMean()
print "beta =",beta_val.GetMean(),", sigFrac =",sigFrac_val.GetMean()
print "mode =",mode
