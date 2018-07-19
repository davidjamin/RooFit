import sys
import ROOT as r

quiet_mode=True
quiet_mode=False

#do_RooFit=True
do_RooFit=False

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

#the_fit_func = "pol5" # old
the_fit_func = "pol7" # good

low_x=50
high_x=250

fitlow_x=55
fithigh_x=200

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
#  4 = alpha sys, fit of bkgd shape from SR -> norm + err shape by +0%
#  5 = alpha sys, fit of bkgd shape from SR -> norm + err shape by -0%
#  6 = alpha sys, fit of bkgd shape from SR -> norm + err shape by +5%
#  7 = alpha sys, fit of bkgd shape from SR -> norm + err shape by -5%
#  8 = alpha sys, fit of bkgd shape from SR -> norm + err shape by +10%
#  9 = alpha sys, fit of bkgd shape from SR -> norm + err shape by -10%
# 10 = alpha sys, fit of bkgd shape from SR -> norm + err shape by +15%
# 11 = alpha sys, fit of bkgd shape from SR -> norm + err shape by -15%
# 12 = alpha sys, fit of bkgd shape from SR -> norm + err shape by +20%
# 13 = alpha sys, fit of bkgd shape from SR -> norm + err shape by -20%
# 14 = alpha sys, fit of bkgd shape from SR -> norm + err shape by +25%
# 15 = alpha sys, fit of bkgd shape from SR -> norm + err shape by -25%
# 16 = alpha sys, fit of bkgd shape from SR -> norm + err shape by +30%
# 17 = alpha sys, fit of bkgd shape from SR -> norm + err shape by -30%
########
# 18 = alpha sys, fit of bkgd shape from SR -> err shape by +0%
# 19 = alpha sys, fit of bkgd shape from SR -> err shape by -0%
# 20 = alpha sys, fit of bkgd shape from SR -> err shape by +5%
# 21 = alpha sys, fit of bkgd shape from SR -> err shape by -5%
# 22 = alpha sys, fit of bkgd shape from SR -> err shape by +10%
# 23 = alpha sys, fit of bkgd shape from SR -> err shape by -10%
# 24 = alpha sys, fit of bkgd shape from SR -> err shape by +15%
# 25 = alpha sys, fit of bkgd shape from SR -> err shape by -15%
# 26 = alpha sys, fit of bkgd shape from SR -> err shape by +20%
# 27 = alpha sys, fit of bkgd shape from SR -> err shape by -20%
# 28 = alpha sys, fit of bkgd shape from SR -> err shape by +25%
# 29 = alpha sys, fit of bkgd shape from SR -> err shape by -25%
# 30 = alpha sys, fit of bkgd shape from SR -> err shape by +30%
# 31 = alpha sys, fit of bkgd shape from SR -> err shape by -30%
########
# 32 = alpha sys, fit of bkgd shape from SR -> shift +5 bins
# 33 = alpha sys, fit of bkgd shape from SR -> shift -5 bins
# 34 = alpha sys, fit of bkgd shape from SR -> shift +4 bins
# 35 = alpha sys, fit of bkgd shape from SR -> shift -4 bins
# 36 = alpha sys, fit of bkgd shape from SR -> shift +3 bins
# 37 = alpha sys, fit of bkgd shape from SR -> shift -3 bins
# 38 = alpha sys, fit of bkgd shape from SR -> shift +2 bins
# 39 = alpha sys, fit of bkgd shape from SR -> shift -2 bins
# 40 = alpha sys, fit of bkgd shape from SR -> shift +1 bins
# 41 = alpha sys, fit of bkgd shape from SR -> shift -1 bins

## if time later
#  = alpha sys, JESup
#  = alpha sys, JESdo
if mode > 41 :
  print "mode="+str(mode)+" not supported -> check !!"
  quit()

def makePseudoExp(p_tth, p_ttz, p_bkg, sig, alpha, ntth, nttz, nbkg, alpha_val, alpha_err):

    if quiet_mode==False: print '================================================================================================='

    # generate datasets
    gen_tth = p_tth.generate(r.RooArgSet(x), ntth, r.RooFit.Extended())
    gen_ttz = p_ttz.generate(r.RooArgSet(x), nttz, r.RooFit.Extended())
    gen_bkg = p_bkg.generate(r.RooArgSet(x), nbkg, r.RooFit.Extended())

    # form template
    d_ttcomb = gen_tth
    d_ttcomb.append(gen_ttz)
    d_ttcomb.append(gen_bkg) # comment here if you don't want bkgd

    ratio = 0.
    ratio_err = 0.

    #########
    # RooFit
    #########
    if do_RooFit==True :
      sig.fitTo(d_ttcomb,r.RooFit.SumW2Error(False),r.RooFit.PrintLevel(-1))
      if quiet_mode==False: print alpha.getVal(), alpha.getError()
      if quiet_mode==False: alpha.Print()
      # invert alpha
      ratio = (1.-alpha.getVal())/alpha.getVal()
      ratio_err = alpha.getError()/alpha.getVal()

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
    if quiet_mode==False: print ratio, ratio_err


x = r.RooRealVar("x", "mjj", low_x, high_x)
frame = x.frame(r.RooFit.Title("sig+bkgd"))


h_tth=infile.Get('ttH_sel'+str(the_sel)+'_'+the_var+the_bin)
if do_Smooth==True : h_tth.Smooth()
d_tth = r.RooDataHist("d_tth", "d_tth", r.RooArgList(x),r.RooFit.Import(h_tth))
p_tth = r.RooHistPdf("p_tth", "p_tth", r.RooArgSet(x),d_tth)
p_tth.plotOn(frame, r.RooFit.LineColor(r.kRed) )

#######ttZ
h_ttz=infile.Get('ttZ_sel'+str(the_sel)+'_'+the_var+the_bin)
if do_Smooth==True : h_ttz.Smooth()
d_ttz = r.RooDataHist("d_ttz", "dttz", r.RooArgList(x),r.RooFit.Import(h_ttz))
p_ttz = r.RooHistPdf("p_ttz", "p_ttz", r.RooArgSet(x),d_ttz)
p_ttz.plotOn(frame, r.RooFit.LineColor(r.kOrange) )

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
if do_Smooth==True : h_ttj.Smooth()
d_ttj = r.RooDataHist("d_ttj", "dttj", r.RooArgList(x),r.RooFit.Import(h_ttj))
p_ttj = r.RooHistPdf("p_ttj", "p_ttj", r.RooArgSet(x),d_ttj)
#p_ttj.plotOn(frame, r.RooFit.LineColor(r.kBlue) )

#######ttbb
h_ttbb=infile.Get('tt+bb_sel'+str(the_sel)+'_'+the_var+the_bin)
if do_Smooth==True : h_ttbb.Smooth()
d_ttbb = r.RooDataHist("d_ttbb", "dttbb", r.RooArgList(x),r.RooFit.Import(h_ttbb))
p_ttbb = r.RooHistPdf("p_ttbb", "p_ttbb", r.RooArgSet(x),d_ttbb)
#p_ttbb.plotOn(frame, r.RooFit.LineColor(r.kViolet) )

# fit tot bkgd for syst
h_ttbkg=h_ttj.Clone()
h_ttbkg.Add(h_ttbb)
myfit = r.TF1("myfit",the_fit_func, low_x, high_x)
h_ttbkg.Fit("myfit","S","",fitlow_x, fithigh_x)
#
percent = 1.
if mode==4  or mode==18: percent = 0.
if mode==5  or mode==19: percent = -0.
if mode==6  or mode==20: percent = 5.
if mode==7  or mode==21: percent = -5.
if mode==8  or mode==22: percent = 10.
if mode==9  or mode==23: percent = -10.
if mode==10 or mode==24: percent = 15.
if mode==11 or mode==25: percent = -15.
if mode==12 or mode==26: percent = 20.
if mode==13 or mode==27: percent = -20.
if mode==14 or mode==28: percent = 25.
if mode==15 or mode==29: percent = -25.
if mode==16 or mode==30: percent = 30.
if mode==17 or mode==31: percent = -30.
percent /= 100.
# the below parl[0]=(Y2-Y1)/(X2-X1)=(1-var_in_Y)/(100-0)
#parl = [-2.*percent/100., 1.+2.*percent]
parl = [percent/25., 1.-4.*percent]

#
my_line = r.TF1("my_line","pol1", low_x, high_x)
my_line.SetParameters(parl[1],parl[0])
h_ttbkg_fit=h_ttbkg.Clone()
h_ttbkg_fiterr=h_ttbkg.Clone()
# find when fit becomes crazy
lowX_min  = myfit.GetMinimumX(0.,100.)
highX_min = myfit.GetMinimumX(100.,300.)
#
for i_bin in xrange( 1, h_ttbkg_fit.GetNbinsX()+1 ):
  bin_val = myfit.Eval(h_ttbkg_fit.GetBinCenter(i_bin))
  if bin_val<0. : bin_val=0.
  if h_ttbkg_fit.GetBinCenter(i_bin)<lowX_min  : bin_val=0.
  if h_ttbkg_fit.GetBinCenter(i_bin)>highX_min : bin_val=0.
  h_ttbkg_fit.SetBinContent(i_bin, bin_val)
  #
  if mode>=0 and mode<=31:
    the_val = my_line.Eval(h_ttbkg_fit.GetBinCenter(i_bin))
    if the_val<0. : the_val=0.
    # use the fit as template
    bin_valerr = bin_val
    # change shape with line
    if mode>=4 : bin_valerr *= the_val
    h_ttbkg_fiterr.SetBinContent(i_bin, bin_valerr)
  # shift shape
  elif mode>=32:
    shift=0
    if mode==32: shift=5
    if mode==33: shift=-5
    if mode==34: shift=4
    if mode==35: shift=-4
    if mode==36: shift=3
    if mode==37: shift=-3
    if mode==38: shift=2
    if mode==39: shift=-2
    if mode==41: shift=1
    if mode==41: shift=-1
    #
    the_val = 0
    i_bin_shift = i_bin-shift
    if i_bin_shift>=1 and i_bin_shift<=h_ttbkg_fit.GetNbinsX():
      the_val = myfit.Eval(h_ttbkg_fit.GetBinCenter(i_bin_shift))
    if the_val<0. : the_val=0.
    h_ttbkg_fiterr.SetBinContent(i_bin, the_val)

# remove fit
if use_fit==False:
  h_ttbkg_fit=h_ttbkg.Clone()
  h_ttbkg_fiterr=h_ttbkg.Clone()

Ninit=h_ttbkg_fit.Integral(low_x, high_x)
Nfiterr=h_ttbkg_fiterr.Integral(low_x, high_x)
if mode<=17: h_ttbkg_fiterr.Scale(Ninit/Nfiterr)
#
d_ttbkg_fit = r.RooDataHist("d_ttbkg", "dttbkg", r.RooArgList(x),r.RooFit.Import(h_ttbkg_fiterr))
p_ttbkg_fit = r.RooHistPdf("p_ttbkg", "p_ttbkg", r.RooArgSet(x),d_ttbkg_fit)

# add pdfs
nbins = h_tth.GetNbinsX()
ntth  = h_tth.Integral( 0,nbins+1)*lumi
nttz  = h_ttz.Integral( 0,nbins+1)*lumi 
nttj  = h_ttj.Integral( 0,nbins+1)*lumi
nttbb = h_ttbb.Integral(0,nbins+1)*lumi
expected=ntth/nttz
#
percent=1.
percent/=100.
if mode==1 :
  nttj*=1.+percent
  nttbb*=1+percent
if mode==2 :
  nttj*=1.-percent
  nttbb*=1.-percent
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
sig = r.RooAddPdf("sig", "Signal", r.RooArgList(p_ttz, p_tth),r.RooArgList(alpha))
#
beta = r.RooRealVar("beta", "background parameter", for_beta, 0., 1.)
beta.setConstant(True)
if mode>=0 :
  bkg = p_ttbkg_fit
# use init template not fit
else:
  bkg = r.RooAddPdf("bkg", "Background", r.RooArgList(p_ttj, p_ttbb),r.RooArgList(beta))
bkg.plotOn(frame, r.RooFit.LineColor(r.kBlue) )
#
sigFrac = r.RooRealVar("sigFrac", "fraction of signal in the tot PDF", for_sigFrac, 0., 1.)
#sigFrac.setConstant(True)
sigBkg = r.RooAddPdf("sigBkg", "Signal+Background", r.RooArgList(sig,bkg),r.RooArgList(sigFrac))

extra = '_STAT'
if mode==1 : extra = '_SCALEup'
if mode==2 : extra = '_SCALEdo'
if mode==3 : extra = '_SHAPECR'
if mode==4 : extra = '_FITSRnorm0up'
if mode==5 : extra = '_FITSRnorm0do'
if mode==6 : extra = '_FITSRnorm5up'
if mode==7 : extra = '_FITSRnorm5do'
if mode==8 : extra = '_FITSRnorm10up'
if mode==9 : extra = '_FITSRnorm10do'
if mode==10: extra = '_FITSRnorm15up'
if mode==11: extra = '_FITSRnorm15do'
if mode==12: extra = '_FITSRnorm20up'
if mode==13: extra = '_FITSRnorm20do'
if mode==14: extra = '_FITSRnorm25up'
if mode==15: extra = '_FITSRnorm25do'
if mode==16: extra = '_FITSRnorm30up'
if mode==17: extra = '_FITSRnorm30do'
if mode==18: extra = '_FITSR0up'
if mode==19: extra = '_FITSR0do'
if mode==20: extra = '_FITSR5up'
if mode==21: extra = '_FITSR5do'
if mode==22: extra = '_FITSR10up'
if mode==23: extra = '_FITSR10do'
if mode==24: extra = '_FITSR15up'
if mode==25: extra = '_FITSR15do'
if mode==26: extra = '_FITSR20up'
if mode==27: extra = '_FITSR20do'
if mode==28: extra = '_FITSR25up'
if mode==29: extra = '_FITSR25do'
if mode==30: extra = '_FITSR30up'
if mode==31: extra = '_FITSR30do'
if mode==32: extra = '_SHIFT5SRup'
if mode==33: extra = '_SHIFT5SRdo'
if mode==34: extra = '_SHIFT4SRup'
if mode==35: extra = '_SHIFT4SRdo'
if mode==36: extra = '_SHIFT3SRup'
if mode==37: extra = '_SHIFT3SRdo'
if mode==38: extra = '_SHIFT2SRup'
if mode==39: extra = '_SHIFT2SRdo'
if mode==40: extra = '_SHIFT1SRup'
if mode==41: extra = '_SHIFT1SRdo'

alpha_val = r.TH1F("alpha_val"+extra, "alpha_val"+extra, 500, 0.0, 3.0)
alpha_err = r.TH1F("alpha_err"+extra, "alpha_err"+extra, 500, 0., 0.1)

n_pseudo = 1
if do_RooFit==True : n_pseudo = 1000
for i in xrange(n_pseudo):
    makePseudoExp(p_tth, p_ttz, bkg, sigBkg, alpha, int(ntth), int(nttz), int(nbkg), alpha_val, alpha_err)


outfile = r.TFile('tth_fit_'+str(mode)+'.root','RECREATE')

if mode==0:
  alpha_exp = r.TH1F("alpha_exp"+extra, "alpha_exp"+extra, 500, 0.0, 3.0)
  alpha_exp.Fill(expected)
  alpha_exp.Write()
alpha_val.Write()
alpha_err.Write()

c = r.TCanvas("plot", "plot", 800, 800)
frame.GetYaxis().SetTitleOffset(1.4)
frame.Draw()
c.SaveAs("sig_bkg_for_fit"+extra+".eps")

# final print
print "alpha =",alpha_val.GetMean(),",",alpha_err.GetMean()
print "mode =",mode
